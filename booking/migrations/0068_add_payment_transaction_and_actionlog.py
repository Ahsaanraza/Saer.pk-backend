from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0067_booking_is_walkin_booking_linked_booking"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="transaction_type",
            field=models.CharField(
                choices=[
                    ("agent_to_branch", "Agent → Branch"),
                    ("area_agent_to_org", "Area Agent → Organization"),
                    ("branch_to_org", "Branch → Organization"),
                    ("org_to_org", "Organization → Organization"),
                ],
                default="agent_to_branch",
                max_length=50,
            ),
        ),

        migrations.CreateModel(
            name="PaymentActionLog",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(choices=[('payment_created', 'Payment Created'), ('payment_approved', 'Payment Approved'), ('payment_rejected', 'Payment Rejected'), ('payment_updated', 'Payment Updated')], max_length=50)),
                ("details", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "payment",
                    models.ForeignKey(
                        related_name="action_logs",
                        on_delete=models.deletion.CASCADE,
                        to="booking.Payment",
                    ),
                ),
                (
                    "performed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
