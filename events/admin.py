from django.contrib import admin

# Register your models here.
from .models import Event, Tag, EventTag
import json


admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(EventTag)
