from django.test import TestCase
from django.contrib.auth.models import User
from organization.models import Organization, Branch, Agency
from booking.models import Booking


class BookingNumberEnforcementTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='TestOrg')
        self.branch = Branch.objects.create(name='Main', organization=self.org)
        self.agency = Agency.objects.create(name='TestAgency', branch=self.branch)
        self.user = User.objects.create(username='testuser2')

    def test_blank_booking_number_raises(self):
        with self.assertRaises(ValueError):
            Booking.objects.create(
                user=self.user,
                organization=self.org,
                branch=self.branch,
                agency=self.agency,
                booking_number='',
                status='Pending',
                total_amount=0
            )

    def test_nan_booking_number_raises(self):
        with self.assertRaises(ValueError):
            Booking.objects.create(
                user=self.user,
                organization=self.org,
                branch=self.branch,
                agency=self.agency,
                booking_number='NaN',
                status='Pending',
                total_amount=0
            )

    def test_valid_booking_number_succeeds(self):
        b = Booking.objects.create(
            user=self.user,
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            booking_number='TEST-BOOK-001',
            status='Pending',
            total_amount=0
        )
        self.assertEqual(b.booking_number, 'TEST-BOOK-001')
