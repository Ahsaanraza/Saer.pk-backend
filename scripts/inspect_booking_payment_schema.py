import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')

django.setup()

from django.db import connection

def cols(table):
    with connection.cursor() as cur:
        try:
            desc = connection.introspection.get_table_description(cur, table)
            return [d.name for d in desc]
        except Exception as e:
            return str(e)

print('booking_payment columns:')
print(cols('booking_payment'))
print('\nbooking_paymentactionlog columns:')
print(cols('booking_paymentactionlog'))
