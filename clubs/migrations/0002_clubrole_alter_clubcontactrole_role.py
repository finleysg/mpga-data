# Generated by Django 4.0.1 on 2022-02-06 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='clubcontactrole',
            name='role',
            field=models.CharField(max_length=30, verbose_name='Role'),
        ),
    ]
