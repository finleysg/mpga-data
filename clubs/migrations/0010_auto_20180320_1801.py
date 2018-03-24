# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-20 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0009_auto_20180121_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='GolfCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Golf Course Name')),
                ('address_txt', models.CharField(blank=True, max_length=200, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=40, verbose_name='City')),
                ('state', models.CharField(blank=True, choices=[('MN', 'Minnesota'), ('WI', 'Wisconsin')], default='MN', max_length=2, verbose_name='State')),
                ('zip', models.CharField(blank=True, max_length=10, verbose_name='Zip Code')),
                ('website', models.CharField(blank=True, max_length=300, verbose_name='Website')),
                ('email', models.CharField(blank=True, max_length=250, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Phone')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='contact',
            name='address_txt',
            field=models.CharField(blank=True, max_length=200, verbose_name='Street Address'),
        ),
        migrations.AddField(
            model_name='contact',
            name='city',
            field=models.CharField(blank=True, max_length=40, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='contact',
            name='state',
            field=models.CharField(blank=True, choices=[('MN', 'Minnesota'), ('WI', 'Wisconsin')], default='MN', max_length=2, verbose_name='State'),
        ),
        migrations.AddField(
            model_name='contact',
            name='use_as_primary',
            field=models.BooleanField(default=False, verbose_name='Use for Club Mailings'),
        ),
        migrations.AddField(
            model_name='contact',
            name='zip',
            field=models.CharField(blank=True, max_length=10, verbose_name='Zip Code'),
        ),
    ]
