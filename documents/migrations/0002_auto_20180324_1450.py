# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-24 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='document',
            name='tags',
        ),
        migrations.AddField(
            model_name='documenttag',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Document', verbose_name='Document'),
        ),
        migrations.AddField(
            model_name='documenttag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Tag', verbose_name='Tag'),
        ),
    ]
