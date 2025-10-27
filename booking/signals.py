from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.db.models import F

from .models import Booking, BookingTicketDetails
from tickets.models import Ticket
from packages.models import UmrahPackage


def _apply_ticket_changes(ticket_id, booked_delta=0, confirmed_delta=0, left_delta=0):
    """Apply deltas to a Ticket using F expressions inside a transaction for safety."""
    with transaction.atomic():
        qs = Ticket.objects.select_for_update().filter(pk=ticket_id)
        if not qs.exists():
            return
        ticket = qs.first()
        if booked_delta:
            ticket.booked_tickets = F('booked_tickets') + booked_delta
        if confirmed_delta:
            ticket.confirmed_tickets = F('confirmed_tickets') + confirmed_delta
        if left_delta:
            ticket.left_seats = F('left_seats') + left_delta
        ticket.save()


def _apply_package_changes(package_id, booked_delta=0, confirmed_delta=0, left_delta=0):
    with transaction.atomic():
        qs = UmrahPackage.objects.select_for_update().filter(pk=package_id)
        if not qs.exists():
            return
        pkg = qs.first()
        if booked_delta:
            pkg.booked_seats = F('booked_seats') + booked_delta
        if confirmed_delta:
            pkg.confirmed_seats = F('confirmed_seats') + confirmed_delta
        if left_delta:
            pkg.left_seats = F('left_seats') + left_delta
        pkg.save()


@receiver(pre_save, sender=Booking)
def booking_pre_save(sender, instance, **kwargs):
    """Cache previous booking state so post_save can compute diffs."""
    if not instance.pk:
        instance._old_booking = None
        return
    try:
        old = Booking.objects.get(pk=instance.pk)
        # cache relevant fields
        instance._old_booking = {
            'status': old.status,
            'total_pax': old.total_pax,
            'ticket_details': list(old.ticket_details.values('ticket_id', 'seats', 'status')),
            'umrah_package_id': old.umrah_package_id,
        }
    except Booking.DoesNotExist:
        instance._old_booking = None


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance, created, **kwargs):
    """Handle seat updates on booking create/update."""
    # helper to sum seats from booking.ticket_details
    def _sum_ticket_seats(details_qs):
        return sum(d.get('seats', 0) for d in details_qs)

    new_status = instance.status
    new_total_pax = instance.total_pax or 0
    # For ticket seat accounting, count only person_details with ticket_included=True
    try:
        ticket_included_count = instance.person_details.filter(ticket_included=True).count()
    except Exception:
        ticket_included_count = None

    old = getattr(instance, '_old_booking', None)

    # On creation: if pending/unpaid -> mark booked seats
    if created:
        if str(new_status).lower() in ['pending', 'unpaid']:
            # tickets: use ticket_included_count if available, otherwise use ticket_details.seats
            if ticket_included_count is not None:
                # allocate included pax across ticket_details: simple allocation proportional to seats
                # fallback: if no ticket_details, skip
                tds = list(instance.ticket_details.all())
                if tds and ticket_included_count > 0:
                    remaining = ticket_included_count
                    for td in tds:
                        assign = min(remaining, td.seats or 0)
                        if assign > 0:
                            _apply_ticket_changes(td.ticket_id, booked_delta=assign, left_delta=-assign)
                            remaining -= assign
                        if remaining <= 0:
                            break
            else:
                for td in instance.ticket_details.all():
                    seats = td.seats or 0
                    if seats > 0:
                        _apply_ticket_changes(td.ticket_id, booked_delta=seats, left_delta=-seats)
            # umrah package: always apply using total_pax
            if instance.umrah_package_id:
                _apply_package_changes(instance.umrah_package_id, booked_delta=new_total_pax, left_delta=-new_total_pax)
        return

    # On update: compare old vs new
    if old:
        old_status = old.get('status')
        old_total_pax = old.get('total_pax') or 0
        old_ticket_details = {d['ticket_id']: d for d in old.get('ticket_details', [])}

        # 2️⃣ Payment / Confirmation: pending/unpaid -> paid/confirmed
        if (str(old_status).lower() in ['pending', 'unpaid']) and (str(new_status).lower() in ['paid', 'confirmed']):
            # for tickets, use ticket_included_count if available
            if ticket_included_count is not None:
                tds = list(instance.ticket_details.all())
                if tds and ticket_included_count > 0:
                    remaining = ticket_included_count
                    for td in tds:
                        assign = min(remaining, td.seats or 0)
                        if assign > 0:
                            _apply_ticket_changes(td.ticket_id, booked_delta=-assign, confirmed_delta=assign)
                            remaining -= assign
                        if remaining <= 0:
                            break
            else:
                for td in instance.ticket_details.all():
                    seats = td.seats or 0
                    if seats > 0:
                        _apply_ticket_changes(td.ticket_id, booked_delta=-seats, confirmed_delta=seats)
            if instance.umrah_package_id:
                _apply_package_changes(instance.umrah_package_id, booked_delta=-new_total_pax, confirmed_delta=new_total_pax)

        # 3️⃣ Cancellation / Expiry
        if str(new_status).lower() in ['cancelled', 'expired']:
            # For tickets: restore left_seats and decrement booked/confirmed depending on old status
            if ticket_included_count is not None:
                tds = list(instance.ticket_details.all())
                if tds and ticket_included_count > 0:
                    remaining = ticket_included_count
                    for td in tds:
                        assign = min(remaining, td.seats or 0)
                        if assign > 0:
                            _apply_ticket_changes(td.ticket_id, left_delta=assign)
                            if str(old_status).lower() in ['pending', 'unpaid']:
                                _apply_ticket_changes(td.ticket_id, booked_delta=-assign)
                            elif str(old_status).lower() in ['paid', 'confirmed']:
                                _apply_ticket_changes(td.ticket_id, confirmed_delta=-assign)
                            remaining -= assign
                        if remaining <= 0:
                            break
            else:
                for td in instance.ticket_details.all():
                    seats = td.seats or 0
                    if seats <= 0:
                        continue
                    # restore availability
                    _apply_ticket_changes(td.ticket_id, left_delta=seats)
                    if str(old_status).lower() in ['pending', 'unpaid']:
                        _apply_ticket_changes(td.ticket_id, booked_delta=-seats)
                    elif str(old_status).lower() in ['paid', 'confirmed']:
                        _apply_ticket_changes(td.ticket_id, confirmed_delta=-seats)
            # Umrah package
            if instance.umrah_package_id:
                _apply_package_changes(instance.umrah_package_id, left_delta=new_total_pax)
                if str(old_status).lower() in ['pending', 'unpaid']:
                    _apply_package_changes(instance.umrah_package_id, booked_delta=-new_total_pax)
                elif str(old_status).lower() in ['paid', 'confirmed']:
                    _apply_package_changes(instance.umrah_package_id, confirmed_delta=-new_total_pax)

        # 4️⃣ Passenger count change (total_pax diff)
        pax_diff = new_total_pax - old_total_pax
        if pax_diff != 0:
            # Positive diff -> reserve more seats (booked +, left -)
            if pax_diff > 0:
                # distribute across umrah package (if exists) and tickets proportionally is complex
                # Simpler: apply to umrah_package if present, else to tickets' first detail
                if instance.umrah_package_id:
                    _apply_package_changes(instance.umrah_package_id, booked_delta=pax_diff, left_delta=-pax_diff)
                else:
                    # allocate to ticket details: add to the first ticket detail
                    td = instance.ticket_details.first()
                    if td:
                        _apply_ticket_changes(td.ticket_id, booked_delta=pax_diff, left_delta=-pax_diff)
            else:
                # reduce reservations
                dec = abs(pax_diff)
                if instance.umrah_package_id:
                    _apply_package_changes(instance.umrah_package_id, booked_delta=-dec, left_delta=dec)
                else:
                    td = instance.ticket_details.first()
                    if td:
                        _apply_ticket_changes(td.ticket_id, booked_delta=-dec, left_delta=dec)


@receiver(post_delete, sender=Booking)
def booking_post_delete(sender, instance, **kwargs):
    """When a booking is deleted, restore seats depending on its status."""
    status = instance.status
    total_pax = instance.total_pax or 0
    # Umrah package
    if instance.umrah_package_id:
        _apply_package_changes(instance.umrah_package_id, left_delta=total_pax)
        if str(status).lower() in ['pending', 'unpaid']:
            _apply_package_changes(instance.umrah_package_id, booked_delta=-total_pax)
        elif str(status).lower() in ['paid', 'confirmed']:
            _apply_package_changes(instance.umrah_package_id, confirmed_delta=-total_pax)



@receiver(post_delete, sender=BookingTicketDetails)
def booking_ticketdetails_post_delete(sender, instance, **kwargs):
    """Adjust ticket counters when a BookingTicketDetails row is deleted (covers cascade deletes)."""
    seats = instance.seats or 0
    if seats <= 0:
        return
    # restore availability
    _apply_ticket_changes(instance.ticket_id, left_delta=seats)
    # prefer booking status (parent) to decide which counters to decrement
    booking_status = getattr(getattr(instance, 'booking', None), 'status', None)
    if booking_status and str(booking_status).lower() in ['pending', 'unpaid']:
        _apply_ticket_changes(instance.ticket_id, booked_delta=-seats)
    elif booking_status and str(booking_status).lower() in ['paid', 'confirmed']:
        _apply_ticket_changes(instance.ticket_id, confirmed_delta=-seats)
    else:
        # fallback: decrement booked_tickets (safer default)
        _apply_ticket_changes(instance.ticket_id, booked_delta=-seats)
