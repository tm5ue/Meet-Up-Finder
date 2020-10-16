from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField
from geopy.geocoders import Nominatim

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=2000, null=True)
    pub_date = models.DateTimeField()
    event_date = models.DateTimeField(null=False, default=timezone.now)
    # start_date = models.DateTimeField(null=False, default=timezone.localtime())
    # end_date = models.DateTimeField(null=False, default=timezone.localtime())
    author = models.CharField(max_length=200, null=False, default="no author")
    invitees = models.ManyToManyField(User)
    location = models.CharField(max_length=2000, null=True)
    tags = models.CharField(max_length=200, null=True)


    def __str__(self):
        return self.name.title()

    def get_location(self):
        geolocator = Nominatim(user_agent="Event")
        location = geolocator.geocode(self.location)
        return location

    def get_latitude(self):
        geolocator = Nominatim(user_agent="Event")
        location = geolocator.geocode(self.location)
        if location is None:
            return location
        else:
            return location.latitude

    def get_longitude(self):
        geolocator = Nominatim(user_agent="Event")
        location = geolocator.geocode(self.location)
        if location is None:
            return location
        else:
            return location.longitude

class Comment(models.Model):
    post = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=200, null=False, default="no author")

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Tag(models.Model):
    tag = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.tag.title()

class EventTag(models.Model):
    e = models.CharField(max_length=200, null=True)
    t = models.CharField(max_length=200, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    def __str__(self):
        return self.event.name.title()
