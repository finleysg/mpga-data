# Generated by Django 2.1.2 on 2018-10-05 02:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPolicy',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('policy_type', models.CharField(choices=[('LR', 'Local Rule'), ('CC', 'Code of Conduct'), ('AU', 'About Us'), ('MP', 'Match Play'), ('TN', 'Tournament'), ('OX', 'Other')], default='OX', max_length=2, verbose_name='Type')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('version', models.IntegerField(default=1, verbose_name='Version')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical policy',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_type', models.CharField(choices=[('LR', 'Local Rule'), ('CC', 'Code of Conduct'), ('AU', 'About Us'), ('MP', 'Match Play'), ('TN', 'Tournament'), ('OX', 'Other')], default='OX', max_length=2, verbose_name='Type')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('version', models.IntegerField(default=1, verbose_name='Version')),
            ],
        ),
    ]
