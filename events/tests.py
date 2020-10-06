from django.test import TestCase, Client
# Create your tests here.
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event
from events.forms import EventForm, inviteForm
from django.db.models import Q
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
        
    def test_invite_valid(self):
        '''valid invitation'''
#        self.client = Client()
#        self.client.login(username='test', password='TestPassword')
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        invited = User.objects.create_user(username='dummyA',
                                    email='a@example.com',
                                    password="TestPassword")
        inviteList = User.objects.all()
        invitation = Event.objects.create(name='bday',
                                     description='fun',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username,
                                     ) #ManytoMany to field is not a valid argument
        invitation.invitees.set(inviteList)
        
        data = {'name': invitation.name,
                'description': invitation.description,
                'event_date': invitation.event_date,
                'invitees':invitation.invitees.all() #querySets always need .all()
                }
        form = inviteForm(data=data)
        self.assertTrue(form.is_valid())
        return data
        
    def test_invite_invalid(self):
        '''valid invitation'''
#        self.client = Client()
#        self.client.login(username='test', password='TestPassword')
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        invited = User.objects.create_user(username='dummyA',
                                    email='a@example.com',
                                    password="TestPassword")
        invitation = Event.objects.create(name='bday',
                                     description='fun',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username,
                                     )
        data = {'name': invitation.name,
                'description': invitation.description,
                'event_date': invitation.event_date,
                'invitees': ''
                }
        form = inviteForm(data=data)
        self.assertFalse(form.is_valid())
        return data
        
    def test_private_invited(self):
        '''displays if invited'''
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        invited = User.objects.create_user(username='dummyA',
                                    email='a@example.com',
                                    password="TestPassword")
        notInvited = User.objects.create_user(username='dummyB',
                                    email='b@example.com',
                                    password="TestPassword")
        invitation = Event.objects.create(name='bday',
                                     description='fun',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username,
                                     )
        invitation.invitees.add(invited)
        l = Event.objects.filter(Q(invitees=invited)).count()
        self.assertEquals(l,1)
        
    def test_private_not_invited(self):
        '''does not display if not invited'''
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        invited = User.objects.create_user(username='dummyA',
                                    email='a@example.com',
                                    password="TestPassword")
        notInvited = User.objects.create_user(username='dummyB',
                                    email='b@example.com',
                                    password="TestPassword")
        invitation = Event.objects.create(name='bday',
                                     description='fun',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username,
                                     )
        invitation.invitees.add(invited)
        l = Event.objects.filter(Q(invitees=notInvited)).count()
        self.assertFalse(l==1)
        
    def test_public_events(self):
        '''displays if there is no specific invitees'''
        event = self.setup()
        l = Event.objects.filter(Q(invitees__isnull=True)).count()
        self.assertEquals(l,1)
