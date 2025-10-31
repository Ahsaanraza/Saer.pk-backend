from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from organization.models import Organization
from tickets.models import Hotels, HotelPrices, HotelContactDetails
from datetime import date, timedelta


class HotelsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # create organization
        self.org = Organization.objects.create(name="OrgTest")
        # create hotel
        today = date.today()
        self.hotel = Hotels.objects.create(
            organization=self.org,
            name="Test Hotel",
            city=None,
            address="123 Test St",
            google_location="",
            video="",
            inventory_owner_organization_id=None,
            reselling_allowed=True,
            contact_number="",
            category="3-star",
            distance=0,
            is_active=True,
            available_start_date=today - timedelta(days=1),
            available_end_date=today + timedelta(days=10),
            status="active",
        )
        # add price
        HotelPrices.objects.create(
            hotel=self.hotel,
            start_date=today,
            end_date=today + timedelta(days=5),
            room_type="Deluxe",
            price=150.0,
            is_sharing_allowed=True,
        )
        # add contact
        HotelContactDetails.objects.create(
            hotel=self.hotel,
            contact_person="John Doe",
            contact_number="123456789",
        )

    def test_hotels_list_returns_expected_json(self):
        url = reverse('hotels-list')
        response = self.client.get(url, {'organization': self.org.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        # find our hotel
        found = False
        for item in data:
            if item.get('name') == self.hotel.name:
                found = True
                # check nested fields
                self.assertIn('prices', item)
                self.assertIsInstance(item['prices'], list)
                self.assertGreaterEqual(len(item['prices']), 1)
                self.assertIn('contact_details', item)
                self.assertIsInstance(item['contact_details'], list)
                self.assertIn('photos_data', item)
                break
        self.assertTrue(found, "Created hotel not found in API response")
