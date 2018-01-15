# Generated by Django 2.0.1 on 2018-01-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0005_auto_20180114_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='payment_type',
            field=models.CharField(choices=[('CK', 'Check'), ('OL', 'Online')], default='CK', max_length=2, verbose_name='Payment Type'),
        ),
    ]
