from django import forms
from django.forms import ModelForm
from .models import Event, Tag, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, HTML
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from location_field.models.plain import PlainLocationField
from geopy.geocoders import Nominatim

class DateInput(forms.DateInput):
    input_type = 'date'

class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Initializes the form with crispy form integration."""
        super(EventForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()

        self.fields['event_date'].widget = DateTimePickerInput()
        for field_name, field in self.fields.items():
            if field_name == 'tags':
                layout.append(Field(field_name, placeholder=field.label+(" (Separated with Semicolons)"), style="width: 100%;"))
            else:
                layout.append(Field(field_name, placeholder=field.label, style="width: 100%;"))
        self.helper.layout.append(Submit('submit', 'Submit Public Event'))

    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date', 'location', 'tags',]
        widgets = {
            'event_date': DateTimePickerInput(),
        }

class EditEventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Initializes the form with crispy form integration."""
        super(EditEventForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()

        self.fields['event_date'].widget = DateTimePickerInput()
        for field_name, field in self.fields.items():
            if field_name == 'tags':
                layout.append(Field(field_name, placeholder=field.label+(" (Separated with Semicolons)"), style="width: 100%;"))
            else:
                layout.append(Field(field_name, placeholder=field.label, style="width: 100%;"))
        self.helper.layout.append(Submit('submit', 'Save Edits'))
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date', 'location', 'tags']
        widgets = {
            'event_date': DateTimePickerInput(),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'description']

class inviteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Initializes the form with crispy form integration."""
        super(inviteForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()

        self.fields['event_date'].widget = DateTimePickerInput()
        for field_name, field in self.fields.items():
            if field_name == 'tags':
                layout.append(Field(field_name, placeholder=field.label+(" (Separated with Semicolons)"), style="width: 100%;"))
            else:
                layout.append(Field(field_name, placeholder=field.label, style="width: 100%;"))
        self.helper.layout.append(Submit('submit', 'Submit Private Event'))

        # self.helper.layout.append(Layout(
        #     ButtonHolder(
        #         Submit('Submit', 'Submit'),
        #         HTML(
        #             '''<a class="btn btn-primary btn-small" href="{% url 'events:myEvents'%}">Submit Private Event</a>''')
        #     )
        # )
        # )
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date', 'location', 'tags', 'invitees']
        widgets = {
            'event_date': DateTimePickerInput(),
        }
    invitees = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
        required=False
    )

 
   
