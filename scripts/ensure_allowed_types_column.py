import os
import django
import sys

# ensure project root is on sys.path when this script is executed from scripts/ directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()
from django.db import connection

table = 'booking_allowedreseller'
column = 'allowed_types'

with connection.cursor() as cursor:
    # check columns
    cursor.execute("SHOW COLUMNS FROM `%s`" % table)
    cols = [row[0] for row in cursor.fetchall()]
    if column in cols:
        print(f"Column {column} already exists on {table}")
        sys.exit(0)
    # try to add JSON column; fall back to LONGTEXT if JSON fails
    try:
        sql = f"ALTER TABLE `{table}` ADD COLUMN `{column}` JSON NULL"
        cursor.execute(sql)
        print(f"Added JSON column {column} to {table}")
    except Exception as e:
        print('Failed to add JSON column, trying LONGTEXT. Error:', e)
        try:
            sql2 = f"ALTER TABLE `{table}` ADD COLUMN `{column}` LONGTEXT NULL"
            cursor.execute(sql2)
            print(f"Added LONGTEXT column {column} to {table}")
        except Exception as e2:
            print('Failed to add LONGTEXT column as well. Error:', e2)
            raise
