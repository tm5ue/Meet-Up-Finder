from django import forms
from django.forms import ModelForm
from .models import Event, Tag
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class EventForm(ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super(EventForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date',]
        # widgets = {
        #     'event_date': DateInput(),
        # }

class inviteForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date','invitees']
    invitees = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple())

 
   
