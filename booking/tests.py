from django.test import TestCase
from decimal import Decimal
from django.utils import timezone

from organization.models import Organization
from packages.models import City
from tickets.models import Hotels
from .models import DiscountGroup, Discount
from .serializers import DiscountGroupSerializer


class DiscountGroupSerializerTest(TestCase):
	def setUp(self):
		# create organization
		self.org = Organization.objects.create(name="Org Test")

		# create a city for hotels
		self.city = City.objects.create(organization=self.org, name="Test City", code="TC")

		# create three hotels
		today = timezone.now().date()
		self.h1 = Hotels.objects.create(
			organization=self.org,
			name="Hotel 1",
			city=self.city,
			address="Addr 1",
			category="3",
			available_start_date=today,
			available_end_date=today + timezone.timedelta(days=30),
		)
		self.h2 = Hotels.objects.create(
			organization=self.org,
			name="Hotel 2",
			city=self.city,
			address="Addr 2",
			category="3",
			available_start_date=today,
			available_end_date=today + timezone.timedelta(days=30),
		)
		self.h3 = Hotels.objects.create(
			organization=self.org,
			name="Hotel 3",
			city=self.city,
			address="Addr 3",
			category="3",
			available_start_date=today,
			available_end_date=today + timezone.timedelta(days=30),
		)

	def test_discountgroup_get_shape(self):
		# create DiscountGroup and discounts to match the example
		dg = DiscountGroup.objects.create(
			name="Ramzan Special",
			group_type="seasonal",
			organization=self.org,
			is_active=True,
		)

		# ticket and umrah package discounts
		Discount.objects.create(
			discount_group=dg,
			organization=self.org,
			things="group_ticket",
			group_ticket_discount_amount=Decimal("1000.00"),
		)
		Discount.objects.create(
			discount_group=dg,
			organization=self.org,
			things="umrah_package",
			umrah_package_discount_amount=Decimal("5000.00"),
		)

		# hotel per-night discounts for the same hotel set
		quint = Discount.objects.create(
			discount_group=dg,
			organization=self.org,
			things="hotel",
			room_type="quint",
			per_night_discount=Decimal("100"),
		)
		quad = Discount.objects.create(
			discount_group=dg,
			organization=self.org,
			things="hotel",
			room_type="quad",
			per_night_discount=Decimal("150"),
		)
		triple = Discount.objects.create(
			discount_group=dg,
			organization=self.org,
			things="hotel",
			room_type="triple",
			per_night_discount=Decimal("200"),
		)
		double = Discount.objects.create(
			discount_group=dg,
			organization=self.org,
			things="hotel",
			room_type="double",
			per_night_discount=Decimal("250"),
		)
		sharing = Discount.objects.create(
			discount_group=dg,
			organization=self.org,
			things="hotel",
			room_type="sharing",
			per_night_discount=Decimal("50"),
		)

		# attach the three hotels to each hotel-discount row
		for d in (quint, quad, triple, double, sharing):
			d.discounted_hotels.set([self.h1, self.h2, self.h3])

		# serialize and assert shape
		data = DiscountGroupSerializer(dg).data

		expected = {
			"id": dg.id,
			"name": "Ramzan Special",
			"group_type": "seasonal",
			"organization": self.org.id,
			"is_active": True,
			"discounts": {
				"group_ticket_discount_amount": "1000.00",
				"umrah_package_discount_amount": "5000.00",
			},
			"hotel_night_discounts": [
				{
					"quint_per_night_discount": "100",
					"quad_per_night_discount": "150",
					"triple_per_night_discount": "200",
					"double_per_night_discount": "250",
					"sharing_per_night_discount": "50",
					"other_per_night_discount": "",
					"discounted_hotels": [self.h1.id, self.h2.id, self.h3.id],
				}
			],
		}

		self.assertEqual(data, expected)
