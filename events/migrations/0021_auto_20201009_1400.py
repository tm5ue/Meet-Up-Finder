# Generated by Django 3.1.1 on 2020-10-09 18:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20201007_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 9, 18, 0, 45, 202695, tzinfo=utc)),
        ),
    ]
