# Generated by Django 2.1.2 on 2019-01-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0014_matchplayresult_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='short_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Short Name'),
        ),
    ]