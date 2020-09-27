from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    # pub_date = models.DateTimeField('date published')
    comments = []

    def __str__(self):
        return self.name.title()

