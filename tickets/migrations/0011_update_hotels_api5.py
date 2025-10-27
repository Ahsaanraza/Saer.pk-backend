from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0010_ticket_inventory_owner_organization_id"),
    ]

    operations = [
        
        # Add new fields to Hotels
        migrations.AddField(
            model_name="hotels",
            name="video",
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="hotels",
            name="inventory_owner_organization_id",
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="hotels",
            name="reselling_allowed",
            field=models.BooleanField(default=False),
        ),
        # Create HotelPhoto model
        migrations.CreateModel(
            name="HotelPhoto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="media/hotel_photos/", null=True, blank=True)),
                ("caption", models.CharField(max_length=255, null=True, blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("hotel", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="photos", to="tickets.hotels")),
            ],
        ),
    ]
