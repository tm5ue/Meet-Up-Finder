from django import forms
from django.forms import ModelForm
from .models import Event, Tag
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from location_field.models.plain import PlainLocationField
from geopy.geocoders import Nominatim

class DateInput(forms.DateInput):
    input_type = 'date'

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date', 'location',]
        widgets = {
            'event_date': DateTimePickerInput(),
        }  

class inviteForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date',]
        widgets = {
            'event_date': DateTimePickerInput(),
        }
    invitees = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
    )

 
   
