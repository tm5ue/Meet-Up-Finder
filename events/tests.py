from django.test import TestCase, Client
# Create your tests here.
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event, Tag, EventTag, Comment
from django.test import Client
from events.forms import EventForm, CommentForm, EditEventForm
from django.db.models import Q
from geopy.geocoders import Nominatim
from django.contrib import auth
from django.urls import reverse
import json

class EventFormTestCase(TestCase):
    def setup(self):
        '''Setup Event testing by creating an Event object with dummy data'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     tags='tag1, tag2, tag3',
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
                'tags': event.tags,
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

class EditEventFormTestCase(TestCase):
    def setup(self):
        '''Setup Event testing by creating an Event object with dummy data'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     tags='tag1, tag2, tag3',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username)
        return event

    def test_valid_event_edit(self):
        '''change the event name'''
        event = self.setup()
        data = {
            'name': "EDITED EVENT",
            'description': event.description,
            'event_date': event.event_date,
            'location': event.get_location(),
            'tags': event.tags,
            }
        form = EditEventForm(data, instance=event)
        if form.is_valid(): form.save()
        self.assertEquals(data['name'], event.name)

    def test_invalied_event_edit(self):
        event = self.setup()
        '''improperly edit'''
        data = {
            'name': "EDITED EVENT",
            'description': event.description,
            'event_date': event.event_date,
            'location': event.get_location(),
            'tags': event.tags,
        }
        form = EditEventForm(data, instance=event)
        # don't save edits
        self.assertNotEquals(data['name'], event.name)

    def test_invalid_event_form(self):
        '''cannot have empty description field'''
        event = self.setup()
        data = {
            'name': "EDITED EVENT",
            'description': "",
            'event_date': event.event_date,
            'location': event.get_location(),
            'tags': event.tags,
        }
        form = EditEventForm(data, instance=event)
        self.assertFalse(form.is_valid())

class CommentFormTestCase(TestCase):
    def setup(self):
        '''Setup Event testing by creating User, Event, and Comment objects with dummy data'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     tags='tag1, tag2, tag3',
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
                                     author=user.username,
                                     tags='tag1, tag2', 
                                     location='Tysons Corner Mall')
        event2 = Event.objects.create(name='two',
                                     description='test description',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username, 
                                     tags='tag2, tag3', 
                                     location='Leesburg Premium Outlets')
        return [event1, event2]

    def test_search_name(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=one')
        returned_events = list(response.context['event_list'])
        self.assertEquals(1, len(returned_events), msg="test_search_name failed: returned "+str(len(returned_events))+" events instead of 1.")
        self.assertEquals(event_list[0], returned_events[0], msg="test_search_name failed: returned "+str(returned_events[0])+" events instead of "+str(event_list[0]))

    def test_search_tag(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=tag1')
        returned_events = list(response.context['event_list'])
        self.assertEquals(1, len(returned_events), msg="test_search_tag failed: returned "+str(len(returned_events))+" events instead of 1.")
        self.assertEquals(event_list[0], returned_events[0], msg="test_search_tag failed: returned "+str(returned_events[0])+" events instead of "+str(event_list[0]))

    def test_search_duplicate(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=tag2')
        returned_events = list(response.context['event_list'])
        self.assertEquals(2, len(returned_events), msg="test_search_duplicate failed: returned "+str(len(returned_events))+" events instead of 2.")

    def test_search_multiple_tags(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=tag1+tag3')
        returned_events = list(response.context['event_list'])
        self.assertEquals(2, len(returned_events), msg="test_search_duplicate failed: returned "+str(len(returned_events))+" events instead of 2.")
    
    def test_search_multiple_names(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=one+two')
        returned_events = list(response.context['event_list'])
        self.assertEquals(2, len(returned_events), msg="test_search_duplicate failed: returned "+str(len(returned_events))+" events instead of 2.")

    def test_search_location(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=Leesburg')
        returned_events = list(response.context['event_list'])
        self.assertEquals(1, len(returned_events), msg="test_search_location failed: returned "+str(len(returned_events))+" events instead of 1.")
        self.assertEquals(event_list[1], returned_events[0], msg="test_search_location failed: returned "+str(returned_events[0])+" events instead of "+str(event_list[0]))

    def test_search_multiple_location(self):
        event_list = self.event_setup()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=Leesburg+Tysons')
        returned_events = list(response.context['event_list'])
        self.assertEquals(2, len(returned_events), msg="test_search_duplicate failed: returned "+str(len(returned_events))+" events instead of 2.")

class InvitesTestCase(TestCase):
    def setup(self):
        '''Setup Event testing by creating an Event object with dummy data'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     tags='tag1, tag2, tag3',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username)
        return event

    def test_invite_valid(self):
        '''valid invitation'''
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        inviteList = User.objects.all()
        invitation = Event.objects.create(name='bday',
                                          description='fun',
                                          tags='tag1, tag2, tag3',
                                          pub_date=timezone.now(),
                                          location="Bodos",
                                          event_date=timezone.now(),
                                          author=user.username,

                                     ) #ManytoMany to field is not a valid argument
        invitation.invitees.set(inviteList)

        data = {'name': invitation.name,
                'description': invitation.description,
                'event_date': invitation.event_date,
                'location': invitation.location,
                'invitees':invitation.invitees.all(), #querySets always need .all()
                'tags': invitation.tags,
                }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
        return data
        
    def test_invite_invalid(self):
        '''invalid invitation'''
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        invitation = Event.objects.create(name='bday',
                                     description='fun',
                                     tags='tag1, tag2, tag3',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username,
                                     )
        data = {'name': invitation.name,
                'description': invitation.description,
                'event_date': invitation.event_date,
                'invitees': '', #makes form invalid
                'tags': invitation.tags,
                }
        form = EventForm(data=data)
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

class Register_BookmarkTest(TestCase):
    def setup(self):
        '''Setup Event testing by creating an Event object with dummy data'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     tags='tag1, tag2, tag3',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=user.username)
        return event

    def test_attend_valid(self):
        '''valid register for event'''
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        attendList = User.objects.all()
        event = Event.objects.create(name='bday',
                                          description='fun',
                                          tags='tag1, tag2, tag3',
                                          pub_date=timezone.now(),
                                          location="Bodos",
                                          event_date=timezone.now(),
                                          author=user.username,

                                     ) #ManytoMany to field is not a valid argument
        event.attendees.set(attendList)

        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                'location': event.location,
                'invitees':event.invitees.all(), #querySets always need .all()
                'tags': event.tags,
                }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
        return data
        
    def test_attend_invalid(self):
        '''invalid register for event'''
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='bday',
                                          description='fun',
                                          tags='tag1, tag2, tag3',
                                          pub_date=timezone.now(),
                                          location="Bodos",
                                          event_date=timezone.now(),
                                          author=user.username,

                                     ) #ManytoMany to field is not a valid argument

        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                'location': event.location,
                'invitees':event.invitees.all(), #querySets always need .all()
                'tags': event.tags,
                }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
        return data
    
    def test_bookmark_valid(self):
        '''valid bookmark'''
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        bookmarkList = User.objects.all()
        event = Event.objects.create(name='bday',
                                          description='fun',
                                          tags='tag1, tag2, tag3',
                                          pub_date=timezone.now(),
                                          location="Bodos",
                                          event_date=timezone.now(),
                                          author=user.username,

                                     ) #ManytoMany to field is not a valid argument
        event.users_bookmarked.set(bookmarkList)

        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                'location': event.location,
                'invitees':event.invitees.all(), #querySets always need .all()
                'tags': event.tags,
                }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
        return data
        
    def test_bookmark_invalid(self):
        '''invalid bookmark'''
        user = User.objects.create_user(username='test',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='bday',
                                          description='fun',
                                          tags='tag1, tag2, tag3',
                                          pub_date=timezone.now(),
                                          location="Bodos",
                                          event_date=timezone.now(),
                                          author=user.username,

                                     ) #ManytoMany to field is not a valid argument

        data = {'name': event.name,
                'description': event.description,
                'event_date': event.event_date,
                'location': event.location,
                'invitees':event.invitees.all(), #querySets always need .all()
                'tags': event.tags,
                }
        form = EventForm(data=data)
        self.assertTrue(form.is_valid())
        return data
        

class EventLocationTestCase(TestCase):
    def setup(self):
        '''Make new event with location'''

        user = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        event = Event.objects.create(name='event test name',
                                     description='test description',
                                     tags='tag1, tag2, tag3',
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
                'tags': event.tags,
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

class SystemsTestCase(TestCase):
    def setup_user(self):
        '''Setup Objects for Systems Testing'''
        self.user1 = User.objects.create_user(username='tester',
                                        email='tester@example.com',
                                        password="TestPassword")
        self.user2 = User.objects.create_user(username='visitor',
                                        email='visitor@example.com',
                                        password="VisitPassword")
    
    def setup_event(self):
        self.event1 = Event.objects.create(name='one',
                                     description='test description',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=self.user1.username,
                                     tags='tag1, tag2', 
                                     location='Tysons Corner Mall')
        self.event2 = Event.objects.create(name='two',
                                     description='test description',
                                     pub_date=timezone.now(),
                                     event_date=timezone.now(),
                                     author=self.user1.username, 
                                     tags='tag2, tag3', 
                                     location='Leesburg Premium Outlets')
    
    def test_systems_case2(self):
        # user story 4: user is able to create an event
        self.setup_user()
        c = Client()
        c.login(username='tester', password='TestPassword')
        # user creates an event
        c.post('/events/add', data={'name':'event test name','description':'test description', 'tags':'tag1, tag2, tag3','event_date':timezone.now(), 'location':'Charlottesville'})
        # system registers event
        self.assertEquals(1, len(Event.objects.all()),  msg="test_systems_case2 failed: added "+str(len(Event.objects.all()))+" events instead of 1.")
        # event shows up on front page
        response = c.get('')
        returned_events = list(response.context['object_list'])
        self.assertEquals(1, len(returned_events), msg="test_systems_case2 failed: returned "+str(len(returned_events))+" events instead of 1.")

    def test_systems_case3(self):
        # user story 4: events are seen by everyone
        # test user creates an event
        self.setup_user()
        c = Client()
        c.login(username='tester', password='TestPassword')
        c.post('/events/add', data={'name':'event test name','description':'test description', 'tags':'tag1, tag2, tag3','event_date':timezone.now(), 'location':'Charlottesville'})
        c.logout()
        # visiting user logs in and sees event
        c.login(username='visitor', password='VisitPassword')
        self.assertEquals(self.user2, auth.get_user(c)) # to ensure that a new user is viewing the events
        response = c.get('')
        returned_events = list(response.context['object_list'])
        self.assertEquals(1, len(returned_events), msg="test_systems_case3 failed: returned "+str(len(returned_events))+" events instead of 1.")
    
    def test_systems_case6(self):
        # user story 3: users can search for events (this test focuses on tags) and access them
        self.setup_user()
        self.setup_event()
        c = Client()
        c.login(username='tester', password='TestPassword')
        response = c.get('/search/?q=tag1')
        returned_events = list(response.context['event_list'])
        # check if the the given event is returned
        self.assertEquals(1, len(returned_events), msg="test_systems_case6 failed: returned "+str(len(returned_events))+" events instead of 1.")
        self.assertEquals(self.event1, returned_events[0], msg="test_systems_case6 failed: returned "+str(returned_events[0])+" events instead of "+str(self.event1))
        # check if the link is in the contents of the returned page
        self.assertTrue('<a href="/events/%d/">One</a>' % self.event1.pk in str(response.content))

    def test_systems_case14(self):
        self.setup_user()
        self.setup_event()
        c = Client()
        c.login(username='tester', password='TestPassword')
        c.post('/events/%d/' % self.event1.pk, data={'name':'test','description':'test comment'})
        # system registers comment
        self.assertEquals(1, len(Comment.objects.all()),  msg="test_systems_case14 failed: added "+str(len(Comment.objects.all()))+" comments instead of 1.")
        # comment shows up on event page
        response = c.get('/events/%d/' % self.event1.pk)
        comments = list(response.context['comments'])
        self.assertEquals(1, len(comments), msg="test_systems_case14 failed: returned "+str(len(comments))+" events instead of 1.")    
    
