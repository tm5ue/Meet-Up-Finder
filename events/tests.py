from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event
from events.forms import EventForm

class EventFormTestCase(TestCase):
    def setup(self):
        '''Setup Event testing by creating an Event object with dummy data'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username)
        return event

    def test_valid_form(self):
        '''Test valid form'''

        event = self.setup()
        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
        return data

    def test_invalid_form(self):
        '''Cannot have an empty name or empty description, thus form is not valid'''

        event = self.setup()
        data = {'name': '',
                'description': '',
                'event_date':  event.event_date}
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        return data
