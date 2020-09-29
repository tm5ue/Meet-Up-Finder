# Generated by Django 3.1.1 on 2020-09-28 02:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='event date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
            preserve_default=False,
        ),
    ]