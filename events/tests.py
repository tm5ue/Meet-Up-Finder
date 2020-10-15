from django.test import TestCase, Client
# Create your tests here.
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event, Tag, EventTag, Comment
from events.forms import EventForm, inviteForm
from django.test import Client
from events.forms import EventForm, inviteForm, CommentForm
from django.db.models import Q
from geopy.geocoders import Nominatim

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
                'location': event.get_location(),
                }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
        return data

    def test_invalid_form(self):
        '''Cannot have an empty name or empty description, thus form is not valid'''
        event = self.setup()
        data = {'name': '',
                'description': '',
                'event_date':  event.event_date,
                'location': event.get_location(),}
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        return data

class CommentFormTestCase(TestCase):
    def setup(self):
        '''Setup Event testing by creating User, Event, and Comment objects with dummy data'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username,
                                     id=1)
        comment = Comment.objects.create(post=event,
                                         name='comment test name',
                                         description='comment test description',
                                         pub_date=timezone.now(),
                                         author=user.username,
                                         post_id=event.id)
        return comment

    def test_valid_comment_form(self):
        '''Valid comment form, has name and description filled'''
        comment = self.setup()
        data = {
            'name': 'comment test',
            'description': 'description test',
            'pub_date': comment.pub_date,
            'author': comment.author,
            'post_id': comment.post_id,
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        '''Invalid comment form, does not have name and description filled'''

        comment = self.setup()
        data = {
            'name': '',
            'description': '',
            'pub_date': comment.pub_date,
            'author': comment.author,
            'post_id': comment.post_id,
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

class TagAdditionTestCase(TestCase):
    def event_setup(self):
        '''Setup an Event with dummy data'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username)
        return event

    def test_valid_tag(self):
        event = self.event_setup()
        tags = {"test1", "test2"}
        event.add_tags(tags)
        num_tags = len(Tag.objects.all())
        num_event_tags = len(event.eventtag_set.all()) 
        self.assertEquals(2, num_tags, msg="test_valid_tag failed: added "+str(num_tags)+" tags to system instead of 2.")
        self.assertEquals(2, num_event_tags, msg="test_valid_tag failed: added "+str(num_event_tags)+" tags to event instead of 2.")

    def test_empty_tag(self):
        event = self.event_setup()
        tags = {""}
        event.add_tags(tags)
        num_tags = len(Tag.objects.all())
        num_event_tags = len(event.eventtag_set.all())
        self.assertEquals(0, num_tags, msg="test_empty_tag failed: added "+str(num_tags)+" tags to system instead of 0.")
        self.assertEquals(0, num_event_tags, msg="test_empty_tag failed: added "+str(num_event_tags)+" tags to event instead of 0.")
    
    def test_duplicate_tag(self):
        event = self.event_setup()
        t = Tag.objects.create(tag="test2") # there is already one in system
        tags = {"test1", "test1", "test2"} # should only add one ("test1")
        event.add_tags(tags)
        num_tags = len(Tag.objects.all())
        num_event_tags = len(event.eventtag_set.all()) 
        self.assertEquals(2, num_tags, msg="test_valid_tag failed: added "+str(num_tags)+" tags to system instead of 1.")
        self.assertEquals(2, num_event_tags, msg="test_valid_tag failed: added "+str(num_event_tags)+" tags to event instead of 2.")

class SearchResultsTestCase(TestCase):
    def event_setup(self):
        '''Setup multiple events with dummy data'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event1 = Event.objects.create(name='one',
                                     description='test description',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username)
        event1.add_tags({"test1", "test2"})
        event2 = Event.objects.create(name='two',
                                     description='test description',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username)
        event2.add_tags({"test2", "test3"})
        return [event1, event2]

    def test_search_name(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=one')
        returned_events = list(response.context['event_list'])
        self.assertEquals(1, len(returned_events), msg="test_search_valid failed: returned "+str(len(returned_events))+" events instead of 1.")
        self.assertEquals(event_list[0], returned_events[0], msg="test_search_valid failed: returned "+str(returned_events[0])+" events instead of "+str(event_list[0]))

    def test_search_tag(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=test1')
        returned_events = list(response.context['event_list'])
        self.assertEquals(1, len(returned_events), msg="test_search_valid failed: returned "+str(len(returned_events))+" events instead of 1.")
        self.assertEquals(event_list[0], returned_events[0], msg="test_search_valid failed: returned "+str(returned_events[0])+" events instead of "+str(event_list[0]))

    def test_search_duplicate(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=test2')
        returned_events = list(response.context['event_list'])
        self.assertEquals(2, len(returned_events), msg="test_search_valid failed: returned "+str(len(returned_events))+" events instead of 2.")

class InvitesTestCase(TestCase):
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

class EventLocationTestCase(TestCase):
    def setup(self):
        '''Make new event with location'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username,
                                     location='Thornton Hall Charlottesville VA',
                                     )
        return event

    def test_valid_form(self):
        '''Test valid form'''

        event = self.setup()
        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                'location': event.location,
                }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
        return data

    def test_invalid_form(self):
        '''Cannot have an location, thus form is not valid'''
        event = self.setup()
        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                'location': '',
                }
        form = EventForm(data=data)
        self.assertFalse(form.is_valid())
        return data
    
    def test_consistent_latitude(self):
        '''Check latitude makes sense'''
        event = self.setup()
        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                'location': event.location,
                }
        geolocator = Nominatim(user_agent="Test")
        loc = geolocator.geocode("Thornton Hall Charlottesville VA")
        self.assertTrue(event.get_latitude() == loc.latitude)
    
    def test_consistent_longitude(self):
        '''Check longitude makes sense'''
        event = self.setup()
        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                'location': event.location,
                }
        geolocator = Nominatim(user_agent="Test")
        loc = geolocator.geocode("Thornton Hall Charlottesville VA")
        self.assertTrue(event.get_longitude() == loc.longitude)
    
    def test_consistent_location(self):
        '''Check location makes sense'''
        event = self.setup()
        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                'location': event.location,
                }
        geolocator = Nominatim(user_agent="Test")
        loc = geolocator.geocode("Thornton Hall Charlottesville VA")
        self.assertTrue(event.get_location() == loc)
