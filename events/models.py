from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=2000, null=True)
    pub_date = models.DateTimeField()
    event_date = models.DateTimeField(null=False, default=timezone.now)
    # start_date = models.DateTimeField(null=False, default=timezone.localtime())
    # end_date = models.DateTimeField(null=False, default=timezone.localtime())
    author = models.CharField(max_length=200, null=False, default="no author")
    # TODO: location (figure out how to integrate maps of some sort similar to https://github.com/caioariede/django-location-field
    # TODO: comments,
    #location =
    #comments = []
    #friends = models.TextField(null=True)
    invitees = models.ManyToManyField(User)


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