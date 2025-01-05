# Generated by Django 5.1.4 on 2025-01-04 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicallandingpage',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical landing page', 'verbose_name_plural': 'historical landing pages'},
        ),
        migrations.AlterField(
            model_name='historicallandingpage',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicallandingpage',
            name='page_type',
            field=models.CharField(choices=[('H', 'Home'), ('B', 'Tournament Bids'), ('A', 'About the MPGA'), ('M', 'Match Play'), ('C', 'Member Clubs'), ('E', 'Club Editing'), ('R', 'Club Registration'), ('I', 'Individual Registration'), ('CC', 'Code of Conduct'), ('OM', 'Our Mission'), ('EC', 'Executive Committee'), ('MP', 'Match Play Signup'), ('FQ', 'FAQ'), ('PP', 'Past Presidents')], max_length=2, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='page_type',
            field=models.CharField(choices=[('H', 'Home'), ('B', 'Tournament Bids'), ('A', 'About the MPGA'), ('M', 'Match Play'), ('C', 'Member Clubs'), ('E', 'Club Editing'), ('R', 'Club Registration'), ('I', 'Individual Registration'), ('CC', 'Code of Conduct'), ('OM', 'Our Mission'), ('EC', 'Executive Committee'), ('MP', 'Match Play Signup'), ('FQ', 'FAQ'), ('PP', 'Past Presidents')], max_length=2, verbose_name='Type'),
        ),
    ]
