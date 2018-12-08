# Generated by Django 2.1.2 on 2018-12-08 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0007_auto_20181208_0914'),
        ('documents', '0002_auto_20181110_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalDocument',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('Admin', 'Admin'), ('Registration', 'Registration'), ('Results', 'Results'), ('Meeting', 'Meeting'), ('Match Play', 'Match Play'), ('Financial', 'Financial'), ('Communications', 'Communications'), ('Other', 'Other')], max_length=20, verbose_name='Document Type')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Golf Season')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('file', models.TextField(max_length=100, verbose_name='File')),
                ('created_by', models.CharField(max_length=100, verbose_name='Created By')),
                ('last_update', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.Event')),
            ],
            options={
                'verbose_name': 'historical document',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPhoto',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('photo_type', models.CharField(choices=[('Committee', 'Committee'), ('Golf Course', 'Golf Course'), ('Tournament Winners', 'Tournament Winners'), ('Tournament Photos', 'Tournament Photos'), ('Other', 'Other')], max_length=20, verbose_name='Type')),
                ('year', models.IntegerField(default=0, verbose_name='Golf Season')),
                ('caption', models.CharField(blank=True, max_length=240, verbose_name='Caption')),
                ('raw_image', models.TextField(max_length=100, verbose_name='Image')),
                ('created_by', models.CharField(max_length=100, verbose_name='Created By')),
                ('last_update', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.Tournament')),
            ],
            options={
                'verbose_name': 'historical photo',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.RemoveField(
            model_name='document',
            name='event',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='event',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='title',
        ),
        migrations.AddField(
            model_name='document',
            name='created_by',
            field=models.CharField(default='', max_length=100, verbose_name='Created By'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents', to='events.Event', verbose_name='Tournament'),
        ),
        migrations.AddField(
            model_name='photo',
            name='caption',
            field=models.CharField(blank=True, max_length=240, verbose_name='Caption'),
        ),
        migrations.AddField(
            model_name='photo',
            name='created_by',
            field=models.CharField(default='', max_length=100, verbose_name='Created By'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='photos', to='events.Tournament', verbose_name='Tournament'),
        ),
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Registration', 'Registration'), ('Results', 'Results'), ('Meeting', 'Meeting'), ('Match Play', 'Match Play'), ('Financial', 'Financial'), ('Communications', 'Communications'), ('Other', 'Other')], max_length=20, verbose_name='Document Type'),
        ),
        migrations.AlterField(
            model_name='documenttag',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='documents.Document', verbose_name='Document'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_type',
            field=models.CharField(choices=[('Committee', 'Committee'), ('Golf Course', 'Golf Course'), ('Tournament Winners', 'Tournament Winners'), ('Tournament Photos', 'Tournament Photos'), ('Other', 'Other')], max_length=20, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='phototag',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='documents.Photo', verbose_name='Photo'),
        ),
    ]
