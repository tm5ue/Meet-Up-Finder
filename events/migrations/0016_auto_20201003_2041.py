# Generated by Django 3.1.1 on 2020-10-04 00:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20201003_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 4, 0, 41, 58, 710168, tzinfo=utc)),
        ),
    ]
