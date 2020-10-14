# Generated by Django 3.1.1 on 2020-10-12 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=2000, null=True)),
                ('pub_date', models.DateTimeField()),
                ('event_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.CharField(default='no author', max_length=200)),
                ('invitees', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e', models.CharField(max_length=200, null=True)),
                ('t', models.CharField(max_length=200, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.tag')),
            ],
        ),
    ]
