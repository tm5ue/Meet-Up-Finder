# Generated by Django 3.1.1 on 2020-10-19 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
    ]