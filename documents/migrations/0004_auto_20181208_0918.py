# Generated by Django 2.1.2 on 2018-12-08 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20181208_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents', to='events.Tournament', verbose_name='Tournament'),
        ),
        migrations.AlterField(
            model_name='historicaldocument',
            name='tournament',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.Tournament'),
        ),
    ]
