# Generated by Django 2.1.2 on 2018-10-04 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Club Name')),
                ('website', models.CharField(blank=True, max_length=300, verbose_name='Website')),
                ('type_2', models.BooleanField(default=False, verbose_name='Type 2')),
                ('size', models.IntegerField(blank=True, null=True, verbose_name='Number of Members')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ClubContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Director of Golf', 'Director of Golf'), ('Event Director', 'Event Director'), ('General Manager', 'General Manager'), ('Handicap Chair', 'Handicap Chair'), ('Manager', 'Manager'), ('Match Play Captain', 'Match Play Captain'), ("Men's Club Contact", "Men's Club Contact"), ("Men's Club President", "Men's Club President"), ("Men's Club Secretary", "Men's Club Secretary"), ("Men's Club Treasurer", "Men's Club Treasurer"), ('Owner', 'Owner'), ('PGA Professional', 'PGA Professional'), ('Sr. Match Play Captain', 'Sr. Match Play Captain'), ('Superintendent', 'Superintendent'), ('Tournament Player', 'Tournament Player'), ('Other', 'Other')], max_length=30, verbose_name='Role')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Primary Contact')),
                ('use_for_mailings', models.BooleanField(default=False, verbose_name='Use for Club Mailings')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='club_to_contact', to='clubs.Club', verbose_name='Club')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('contact_type', models.CharField(choices=[("Men's Club", "Men's Club"), ('Facilities', 'Facilities'), ('Allied Association', 'Allied Association'), ('Executive Committee', 'Executive Committee')], default="Men's Club", max_length=20, verbose_name='Contact Type')),
                ('primary_phone', models.CharField(blank=True, max_length=20, verbose_name='Primary Phone')),
                ('alternate_phone', models.CharField(blank=True, max_length=20, verbose_name='Alternate Phone')),
                ('email', models.CharField(blank=True, max_length=250, verbose_name='Email')),
                ('address_txt', models.CharField(blank=True, max_length=200, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=40, verbose_name='City')),
                ('state', models.CharField(blank=True, choices=[('IA', 'Iowa'), ('MN', 'Minnesota'), ('ND', 'North Dakota'), ('SD', 'South Dakota'), ('WI', 'Wisconsin')], default='MN', max_length=2, verbose_name='State')),
                ('zip', models.CharField(blank=True, max_length=10, verbose_name='Zip Code')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
        ),
        migrations.CreateModel(
            name='GolfCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Golf Course Name')),
                ('address_txt', models.CharField(blank=True, max_length=200, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=40, verbose_name='City')),
                ('state', models.CharField(blank=True, choices=[('IA', 'Iowa'), ('MN', 'Minnesota'), ('ND', 'North Dakota'), ('SD', 'South Dakota'), ('WI', 'Wisconsin')], default='MN', max_length=2, verbose_name='State')),
                ('zip', models.CharField(blank=True, max_length=10, verbose_name='Zip Code')),
                ('website', models.CharField(blank=True, max_length=300, verbose_name='Website')),
                ('email', models.CharField(blank=True, max_length=250, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Phone')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='Golf Season')),
                ('payment_date', models.DateField(verbose_name='Payment Date')),
                ('payment_type', models.CharField(choices=[('CK', 'Check'), ('OL', 'Online'), ('CA', 'Cash')], default='CK', max_length=2, verbose_name='Payment Type')),
                ('payment_code', models.CharField(blank=True, max_length=20, verbose_name='Code or Number')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Recorded')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='memberships', to='clubs.Club', verbose_name='Club')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='Golf Season')),
                ('group_name', models.CharField(max_length=20, verbose_name='Group')),
                ('is_senior', models.BooleanField(verbose_name='Senior')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='teams', to='clubs.Club', verbose_name='Club')),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='clubs.Contact', verbose_name='Captain')),
            ],
        ),
        migrations.AddField(
            model_name='clubcontact',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contact_to_club', to='clubs.Contact', verbose_name='Contact'),
        ),
        migrations.AddField(
            model_name='club',
            name='contacts',
            field=models.ManyToManyField(through='clubs.ClubContact', to='clubs.Contact', verbose_name='Contacts'),
        ),
        migrations.AddField(
            model_name='club',
            name='golf_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='clubs.GolfCourse', verbose_name='Home Course'),
        ),
    ]
