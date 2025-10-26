from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from organization.models import Organization, Branch, Agency
from packages.models import City, Airlines
from tickets.models import Ticket
from booking.models import Booking, BookingTicketDetails, BookingPersonDetail


User = get_user_model()


class AutoSeatManagementTests(TestCase):
    def setUp(self):
        # create minimal fixtures
        self.user = User.objects.create(username='tester')
        self.org = Organization.objects.create(name='Org A')
        self.branch = Branch.objects.create(organization=self.org, name='Main')
        self.branch.user.add(self.user)
        self.agency = Agency.objects.create(branch=self.branch, name='Agency1')

        # City requires an organization and a code in this project
        self.city = City.objects.create(name='CityX', organization=self.org, code='C1')

        # create an airline and a ticket
        self.airline = Airlines.objects.create(organization=self.org, name='Air1', code='A1')
        self.ticket = Ticket.objects.create(
            organization=self.org,
            airline=self.airline,
            pnr='PNR1',
            total_seats=10,
            left_seats=10,
            booked_tickets=0,
            confirmed_tickets=0,
            trip_type='oneway',
            departure_stay_type='d',
            return_stay_type='r',
            weight=0,
            pieces=0,
        )

    def test_new_booking_reserves_seats(self):
        b = Booking.objects.create(
            user=self.user,
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            booking_number='B1',
            total_pax=2,
            status='pending',
            expiry_time=timezone.now() + timezone.timedelta(days=1),
        )
        # add booking ticket details
        btd = BookingTicketDetails.objects.create(booking=b, ticket=self.ticket, seats=2)
        # add person details (ticket_included True)
        BookingPersonDetail.objects.create(booking=b, first_name='P1', ticket_included=True)
        BookingPersonDetail.objects.create(booking=b, first_name='P2', ticket_included=True)

        # refresh ticket
        t = Ticket.objects.get(pk=self.ticket.pk)
        self.assertEqual(t.booked_tickets, 2)
        self.assertEqual(t.left_seats, 8)

    def test_payment_moves_booked_to_confirmed(self):
        b = Booking.objects.create(
            user=self.user,
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            booking_number='B2',
            total_pax=1,
            status='pending',
            expiry_time=timezone.now() + timezone.timedelta(days=1),
        )
        BookingTicketDetails.objects.create(booking=b, ticket=self.ticket, seats=1)
        BookingPersonDetail.objects.create(booking=b, first_name='P1', ticket_included=True)
        # pay/confirm
        b.status = 'paid'
        b.save()
        t = Ticket.objects.get(pk=self.ticket.pk)
        self.assertEqual(t.booked_tickets, 0)
        self.assertEqual(t.confirmed_tickets, 1)

    def test_cancellation_restores_seats(self):
        b = Booking.objects.create(
            user=self.user,
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            booking_number='B3',
            total_pax=1,
            status='pending',
            expiry_time=timezone.now() + timezone.timedelta(days=1),
        )
        BookingTicketDetails.objects.create(booking=b, ticket=self.ticket, seats=1)
        BookingPersonDetail.objects.create(booking=b, first_name='P1', ticket_included=True)
        # cancel
        b.status = 'cancelled'
        b.save()
        t = Ticket.objects.get(pk=self.ticket.pk)
        self.assertEqual(t.booked_tickets, 0)
        self.assertEqual(t.left_seats, 10)

    def test_edit_pax_changes_seats(self):
        b = Booking.objects.create(
            user=self.user,
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            booking_number='B4',
            total_pax=1,
            status='pending',
            expiry_time=timezone.now() + timezone.timedelta(days=1),
        )
        BookingTicketDetails.objects.create(booking=b, ticket=self.ticket, seats=1)
        BookingPersonDetail.objects.create(booking=b, first_name='P1', ticket_included=True)
        t = Ticket.objects.get(pk=self.ticket.pk)
        self.assertEqual(t.left_seats, 9)
        # increase pax to 2
        b.total_pax = 2
        BookingPersonDetail.objects.create(booking=b, first_name='P2', ticket_included=True)
        b.save()
        t.refresh_from_db()
        self.assertEqual(t.booked_tickets, 2)
        self.assertEqual(t.left_seats, 8)

    def test_delete_booking_restores(self):
        b = Booking.objects.create(
            user=self.user,
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            booking_number='B5',
            total_pax=1,
            status='pending',
            expiry_time=timezone.now() + timezone.timedelta(days=1),
        )
        BookingTicketDetails.objects.create(booking=b, ticket=self.ticket, seats=1)
        BookingPersonDetail.objects.create(booking=b, first_name='P1', ticket_included=True)
        b.delete()
        t = Ticket.objects.get(pk=self.ticket.pk)
        self.assertEqual(t.booked_tickets, 0)
        self.assertEqual(t.left_seats, 10)
from django.test import TestCase

# Create your tests here.
