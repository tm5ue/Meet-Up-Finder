from django.contrib import admin

# Register your models here.
from .models import Event, Tag, EventTag, Comment
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(EventTag)
admin.site.register(Comment)
