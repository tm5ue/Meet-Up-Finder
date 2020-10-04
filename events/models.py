from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    pub_date = models.DateTimeField()
    event_date = models.DateTimeField(null=False, default=timezone.localtime())
    # start_date = models.DateTimeField(null=False, default=timezone.localtime())
    # end_date = models.DateTimeField(null=False, default=timezone.localtime())
    author = models.CharField(max_length=200, null=False, default="no author")
    # TODO: fix date input field (find interactive calendar to input date and time)
    # TODO: location (figure out how to integrate maps of some sort similar to https://github.com/caioariede/django-location-field
    # TODO: comments,
    # TODO: tags (sports, music, etc)
    #location =
    #comments = []
    friends = models.TextField(null=True)
    users = models.ManyToManyField(User)



    def __str__(self):
        return self.name.title()

