from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from organization.models import Organization, Branch, Agency
from .models import Booking
from users.models import UserProfile
from finance.utils import calculate_profit_loss
from finance.models import FinancialRecord


class WalkinBookingTests(TestCase):
    def setUp(self):
        # base objects
        self.user = User.objects.create_user(username='walkuser', password='pass')
        UserProfile.objects.create(user=self.user)
        self.org = Organization.objects.create(name='WalkOrg')
        self.branch = Branch.objects.create(name='Main', organization=self.org)
        self.agency = Agency.objects.create(name='A1', branch=self.branch)

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_walkin_permission_denied_for_regular_user(self):
        payload = {
            'booking_number': 'WALK-001',
            'status': 'Pending',
            'agency_id': self.agency.id,
            'user_id': self.user.profile.id,
        }
        resp = self.client.post('/api/bookings/walkin/', payload, format='json')
        self.assertEqual(resp.status_code, 403)

    def test_link_permission_and_linking_behavior(self):
        # create two bookings
        main = Booking.objects.create(
            user=self.user, organization=self.org, branch=self.branch, agency=self.agency,
            booking_number='BK-MAIN', status='Pending'
        )
        walkin = Booking.objects.create(
            user=self.user, organization=self.org, branch=self.branch, agency=self.agency,
            booking_number='BK-WALK', status='Pending', is_walkin=True
        )

        # normal user cannot link
        resp = self.client.post(f'/api/bookings/{walkin.id}/link/', {'linked_booking_id': main.id}, format='json')
        self.assertEqual(resp.status_code, 403)

        # add finance_managers group -> allow
        grp, _ = Group.objects.get_or_create(name='finance_managers')
        self.user.groups.add(grp)

        resp2 = self.client.post(f'/api/bookings/{walkin.id}/link/', {'linked_booking_id': main.id}, format='json')
        self.assertEqual(resp2.status_code, 200)

        walkin.refresh_from_db()
        self.assertIsNotNone(walkin.linked_booking)
        self.assertEqual(walkin.linked_booking.id, main.id)

    def test_financial_record_includes_linked_booking_metadata(self):
        main = Booking.objects.create(
            user=self.user, organization=self.org, branch=self.branch, agency=self.agency,
            booking_number='BK-MAIN-2', status='Pending'
        )
        walkin = Booking.objects.create(
            user=self.user, organization=self.org, branch=self.branch, agency=self.agency,
            booking_number='BK-WALK-2', status='Pending', is_walkin=True, linked_booking=main
        )

        # run profit/loss calculation for the walkin (should record metadata)
        fr = calculate_profit_loss(walkin.id)
        self.assertIsNotNone(fr)
        self.assertIn('linked_booking_id', fr.metadata)
        self.assertEqual(fr.metadata.get('linked_booking_id'), main.id)
