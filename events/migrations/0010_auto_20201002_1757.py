# Generated by Django 3.1.1 on 2020-10-02 21:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20201002_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 2, 21, 57, 22, 653578, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='friends',
            field=models.TextField(null=True),
        ),
    ]
