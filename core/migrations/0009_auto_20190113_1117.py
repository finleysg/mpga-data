# Generated by Django 2.1.2 on 2019-01-13 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_seasonsettings_match_play_forfeit_percentage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seasonsettings',
            options={'verbose_name': 'Season Settings', 'verbose_name_plural': 'Season Settings'},
        ),
    ]