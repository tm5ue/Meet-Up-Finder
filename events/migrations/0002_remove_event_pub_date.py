# Generated by Django 3.1.1 on 2020-09-27 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='pub_date',
        ),
    ]
