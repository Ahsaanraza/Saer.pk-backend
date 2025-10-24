from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Ticket
from booking.models import BookingTicketDetails 
from django.db import models

@receiver(post_save, sender=BookingTicketDetails)
def update_ticket_on_booking_save(sender, instance, created, **kwargs):
    ticket = instance.ticket
    seats = instance.seats

    booked = BookingTicketDetails.objects.filter(ticket=ticket, status="booked").aggregate(total=models.Sum("seats"))["total"] or 0
    confirmed = BookingTicketDetails.objects.filter(ticket=ticket, status="confirmed").aggregate(total=models.Sum("seats"))["total"] or 0
    cancelled = BookingTicketDetails.objects.filter(ticket=ticket, status="cancelled").aggregate(total=models.Sum("seats"))["total"] or 0

    ticket.booked_tickets = booked
    ticket.confirmed_tickets = confirmed
    ticket.available_seats = ticket.total_seats - (booked + confirmed)
    ticket.save()


@receiver(post_delete, sender=BookingTicketDetails)
def update_ticket_on_booking_delete(sender, instance, **kwargs):
    ticket = instance.ticket

    booked = BookingTicketDetails.objects.filter(ticket=ticket, status="booked").aggregate(total=models.Sum("seats"))["total"] or 0
    confirmed = BookingTicketDetails.objects.filter(ticket=ticket, status="confirmed").aggregate(total=models.Sum("seats"))["total"] or 0

    ticket.booked_tickets = booked
    ticket.confirmed_tickets = confirmed
    ticket.available_seats = ticket.total_seats - (booked + confirmed)
    ticket.save()
