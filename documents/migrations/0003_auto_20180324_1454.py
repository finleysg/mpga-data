# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-24 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20180324_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Golf Season'),
        ),
    ]
