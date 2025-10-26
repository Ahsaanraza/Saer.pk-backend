from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0011_update_hotels_api5"),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='owner_organization_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='reselling_allowed',
            field=models.BooleanField(default=False),
        ),
    ]
