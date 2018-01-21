# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-21 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0008_team_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubcontact',
            name='role',
            field=models.CharField(choices=[('Director of Golf', 'Director of Golf'), ('Event Director', 'Event Director'), ('General Manager', 'General Manager'), ('Handicap Chair', 'Handicap Chair'), ('Manager', 'Manager'), ('Match Play Captain', 'Match Play Captain'), ("Men's Club Contact", "Men's Club Contact"), ("Men's Club President", "Men's Club President"), ("Men's Club Secretary", "Men's Club Secretary"), ("Men's Club Treasurer", "Men's Club Treasurer"), ('Owner', 'Owner'), ('PGA Professional', 'PGA Professional'), ('Sr. Match Play Captain', 'Sr. Match Play Captain'), ('Superintendent', 'Superintendent')], max_length=30, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='contact_type',
            field=models.CharField(choices=[("Men's Club", "Men's Club"), ('Facilities', 'Facilities'), ('Allied Association', 'Allied Association'), ('Executive Committee', 'Executive Committee')], default="Men's Club", max_length=20, verbose_name='Contact Type'),
        ),
    ]
