# Generated by Django 2.1.2 on 2019-01-13 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0016_auto_20190113_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='address_txt',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Street Address'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='alternate_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Alternate Phone'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='primary_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Primary Phone'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='state',
            field=models.CharField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='MN', max_length=2, null=True, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='zip',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Zip Code'),
        ),
    ]
