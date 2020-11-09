from django import forms
from django.forms import ModelForm
from .models import Event, Tag, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, HTML
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DateTimePickerInput
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
           self.fields['photo'].required = False
           self.fields['invitees'].required = False
           self.fields['tags'].required = False
           self.fields['event_date'].widget = DateTimePickerInput()
           for field_name, field in self.fields.items():
               if field_name == 'tags':
                   layout.append(Field(field_name, placeholder=field.label+(" (Separated with Commas)"), style="width: 100%;"))
               else:
                   layout.append(Field(field_name, placeholder=field.label, style="width: 100%;"))
           self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary btn-sm'))

       class Meta:
           model = Event

           fields = ['name', 'description', 'event_date', 'location', 'tags', 'invitees', 'photo']

           widgets = {
               'event_date': DateTimePickerInput(),
           }
       invitees = forms.ModelMultipleChoiceField(
           queryset = User.objects.all(),
           widget = forms.CheckboxSelectMultiple(),
           required=False
       )


class EditEventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Initializes the form with crispy form integration."""
        super(EditEventForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout()
        self.fields['invitees'].required = False
        self.fields['event_date'].widget = DateTimePickerInput()
        self.fields['tags'].required = False
        self.fields['photo'].required = False
        for field_name, field in self.fields.items():
            if field_name == 'tags':
                layout.append(Field(field_name, placeholder=field.label+(" (Separated with Commas)"), style="width: 100%;"))
            else:
                layout.append(Field(field_name, placeholder=field.label, style="width: 100%;"))
        self.helper.layout.append(ButtonHolder(
            Submit('submit', 'Save Edits', css_class='btn-primary btn-sm'),
            HTML("""<a href="{% url 'events:delete_event' event.id %}" class="btn-danger btn-sm" >Delete Event</a>""")))
        self.helper.form_method = 'POST'

    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date', 'location', 'tags', 'invitees', 'photo']
        widgets = {
            'event_date': DateTimePickerInput(),
        }
    invitees = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
        )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'description']