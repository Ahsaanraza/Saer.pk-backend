from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassportLead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_id', models.IntegerField(db_index=True)),
                ('organization_id', models.IntegerField(db_index=True)),
                ('lead_source', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_name', models.CharField(max_length=200)),
                ('customer_phone', models.CharField(db_index=True, max_length=30)),
                ('cnic', models.CharField(blank=True, db_index=True, max_length=20, null=True)),
                ('passport_number', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('followup_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('converted', 'Converted')], default='pending', max_length=20)),
                ('next_followup_date', models.DateField(blank=True, db_index=True, null=True)),
                ('pending_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('is_deleted', models.BooleanField(db_index=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
            options={'db_table': 'passport_lead'},
        ),
        migrations.CreateModel(
            name='PaxProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('passport_number', models.CharField(db_index=True, max_length=50)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pax', to='passport_leads.passportlead')),
            ],
            options={'db_table': 'pax_profile'},
        ),
        migrations.CreateModel(
            name='FollowUpLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followups', to='passport_leads.passportlead')),
            ],
            options={'db_table': 'followup_log'},
        ),
        migrations.AddIndex(
            model_name='passportlead',
            index=models.Index(fields=['customer_phone'], name='passportlead_custph_idx'),
        ),
        migrations.AddIndex(
            model_name='passportlead',
            index=models.Index(fields=['passport_number'], name='passportlead_pass_idx'),
        ),
        migrations.AddIndex(
            model_name='passportlead',
            index=models.Index(fields=['cnic'], name='passportlead_cnic_idx'),
        ),
        migrations.AddIndex(
            model_name='passportlead',
            index=models.Index(fields=['branch_id'], name='passportlead_branch_idx'),
        ),
        migrations.AddIndex(
            model_name='passportlead',
            index=models.Index(fields=['next_followup_date'], name='passportlead_nextf_idx'),
        ),
        migrations.AddIndex(
            model_name='paxprofile',
            index=models.Index(fields=['passport_number'], name='paxprofile_pass_idx'),
        ),
    ]
