from django.db import models
from django.contrib.sites.models import Site

# Create your models here.
class Location(models.Model):
    city = models.TextField(null=True)

