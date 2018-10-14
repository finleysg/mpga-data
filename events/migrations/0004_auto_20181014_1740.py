# Generated by Django 2.1.2 on 2018-10-14 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20181014_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='alt_event_fee',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_fee',
        ),
        migrations.RemoveField(
            model_name='event',
            name='portal_url',
        ),
        migrations.RemoveField(
            model_name='event',
            name='registration_url',
        ),
        migrations.RemoveField(
            model_name='historicalevent',
            name='alt_event_fee',
        ),
        migrations.RemoveField(
            model_name='historicalevent',
            name='event_fee',
        ),
        migrations.RemoveField(
            model_name='historicalevent',
            name='portal_url',
        ),
        migrations.RemoveField(
            model_name='historicalevent',
            name='registration_url',
        ),
        migrations.AddField(
            model_name='eventfee',
            name='ec_only',
            field=models.BooleanField(default=False, verbose_name='Only EC members see this'),
        ),
        migrations.AddField(
            model_name='eventlink',
            name='title',
            field=models.CharField(default='TM Portal', max_length=60, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='eventlink',
            name='link_type',
            field=models.CharField(choices=[('Results', 'Results'), ('Tee Times', 'Tee Times'), ('Registration', 'Registration'), ('Media', 'Media')], max_length=40, verbose_name='Link Type'),
        ),
    ]
