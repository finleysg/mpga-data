# Generated by Django 2.1.5 on 2020-01-19 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0017_auto_20190113_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clubcontact',
            options={'ordering': ['contact__last_name', 'contact__first_name']},
        ),
        migrations.AlterModelOptions(
            name='membership',
            options={'ordering': ['-year', 'club__name']},
        ),
    ]