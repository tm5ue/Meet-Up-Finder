from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField
from geopy.geocoders import Nominatim
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
# Create your models here.

class Event(models.Model):
    upload_storage = FileSystemStorage(location=settings.UPLOAD_ROOT, base_url='/images')

    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=2000, null=True)
    pub_date = models.DateTimeField()
    event_date = models.DateTimeField(null=False, default=timezone.now)
    # start_date = models.DateTimeField(null=False, default=timezone.localtime())
    # end_date = models.DateTimeField(null=False, default=timezone.localtime())
    author = models.CharField(max_length=200, null=False, default="no author")
    invitees = models.ManyToManyField(User, null=True, blank=True)
    users_bookmarked = models.ManyToManyField(User, related_name="bookmarked_users")
    attendees = models.ManyToManyField(User, related_name="users_attending")
    location = models.CharField(max_length=2000, null=True)
    tags = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    photo = models.ImageField(null=True, upload_to='images', storage=upload_storage, max_length=750)
    photourl = models.CharField(max_length=1000, null=True)

    def add_tags(self, t):
        ''' Add tags from a list to the given event '''
        t_set = set(t) # eliminate duplicates
        if next(iter(t_set)) != "":
            for tag_whitespace in t_set:
                tag = tag_whitespace.strip() # remove leading and trailing whitespace
                if not Tag.objects.filter(tag=tag):
                    t = Tag(tag=tag)
                    t.save()
                et = EventTag(e=self.name, t=tag, event=self, tag=Tag.objects.get(tag=tag))
                et.save()

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
        return 'Comment {} by {}'.format(self.description, self.author)

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
