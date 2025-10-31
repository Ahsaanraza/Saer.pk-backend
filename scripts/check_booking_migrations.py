import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')

django.setup()

from django.db import connection

with connection.cursor() as cur:
    cur.execute("SELECT app, name, applied FROM django_migrations WHERE app='booking' ORDER BY applied")
    rows = cur.fetchall()

print('Applied booking migrations:')
for r in rows:
    print(r)
