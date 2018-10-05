# Generated by Django 2.1.2 on 2018-10-04 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRegistration',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('event_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Event fee')),
                ('is_event_fee_paid', models.BooleanField(default=False, verbose_name='Event fee paid')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('event', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.Event')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Member')),
            ],
            options={
                'verbose_name': 'historical registration',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalRegistrationGroup',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('notes', models.TextField(blank=True, verbose_name='Registration notes')),
                ('card_verification_token', models.CharField(blank=True, max_length=30, verbose_name='Card verification token')),
                ('payment_confirmation_code', models.CharField(blank=True, max_length=30, verbose_name='Payment confirmation code')),
                ('payment_confirmation_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Payment confirmation timestamp')),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Payment amount')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('event', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.Event')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('signed_up_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Member')),
            ],
            options={
                'verbose_name': 'historical registration group',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Event fee')),
                ('is_event_fee_paid', models.BooleanField(default=False, verbose_name='Event fee paid')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='events.Event', verbose_name='Event')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Member', verbose_name='Member')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, verbose_name='Registration notes')),
                ('card_verification_token', models.CharField(blank=True, max_length=30, verbose_name='Card verification token')),
                ('payment_confirmation_code', models.CharField(blank=True, max_length=30, verbose_name='Payment confirmation code')),
                ('payment_confirmation_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Payment confirmation timestamp')),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Payment amount')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Event')),
                ('signed_up_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Member', verbose_name='Signed up by')),
            ],
        ),
        migrations.AddField(
            model_name='registration',
            name='registration_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='register.RegistrationGroup', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='historicalregistration',
            name='registration_group',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='register.RegistrationGroup'),
        ),
    ]
