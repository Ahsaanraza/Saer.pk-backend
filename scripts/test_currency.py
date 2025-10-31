import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','configuration.settings')
import django
django.setup()
from ledger.currency_utils import convert_sar_to_pkr
print('convert_sar_to_pkr imported:', callable(convert_sar_to_pkr))
try:
    # try with dummy values; will likely raise if no RiyalRate exists
    # but we just want to ensure function runs until rate fetch
    from packages.models import RiyalRate
    print('RiyalRate model available')
except Exception as e:
    print('RiyalRate import failed:', e)
