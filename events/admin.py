from django.contrib import admin

# Register your models here.
from .models import Event, Tag, EventTag
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
import json


admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(EventTag)

class RentalAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }