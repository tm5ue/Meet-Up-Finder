from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView, View
from django.utils import timezone
from .models import Event, Tag, EventTag, Comment
from .forms import EventForm, CommentForm, EditEventForm #,BookmarkForm#,inviteForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_datepicker_plus import DateTimePickerInput
from django import template
from django.conf import settings
from functools import reduce
from operator import or_
from django.core.mail import send_mass_mail, send_mail
import re

class Index(ListView):
    '''Class for home page'''
    template_name = 'events/index.html'
    Model=Event
    def get_queryset(self):
        '''
        Get public Events to display on home page
        :return:
        '''
        return Event.objects.filter(Q(invitees__isnull=True)) #public events

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

class SearchResultsView(ListView):
    model = Event
    template_name = 'events/search_results.html'
    def get_queryset(self):
        '''Get search criteria and return list of corresponding events'''
        queries = normalize_query(self.request.GET.get('q'))
        user = User.objects.get(email=self.request.user.email)
        name_query = reduce(or_, (Q(name__icontains=query) for query in queries))
        tag_query = reduce(or_, (Q(tags__icontains=query) for query in queries))
        location_query = reduce(or_, (Q(location__icontains=query) for query in queries))
        event_list = Event.objects.filter(
            (Q(invitees__isnull=True) | Q(invitees=user) | Q(author=user)) & #either public/invited events/events you wrote
            (name_query | tag_query | location_query)
        ).distinct()
        return event_list
    # TODO: add filtering

class AddEvent(TemplateView):
    template_name = 'events/add_event.html'
    def post(self, request):
        '''Handles adding a new event'''
        form = EventForm(request.POST, request.FILES)
        tags = request.POST.get('tags', None).split(",")
        tags = [tag.title().strip() for tag in tags]
        tags = set(tags)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.pub_date = timezone.localtime()
            event.tags = ", ".join(tags)
            event.email = request.user.email
            event.photourl = 'https://meetup-finder-static.s3.amazonaws.com/media/images/{}'.format(event.photo.name)
            event.save()
            event.add_tags(tags)
        context = {'form': form}
        if(not event.invitees.all()):
            return redirect('/events/{}'.format(event.id))
        else:
            return redirect('/events/myEvents')

    def get(self, request):
        '''Handles displaying the empty form'''
        form = EventForm()
        return render(request, self.template_name, {'form': form})
    def get_queryset(self):
        pass

class AddEvent(TemplateView):
    template_name = 'events/add_event.html'
    def post(self, request):
        '''Handles adding a new event'''
        event_items = {
            "name": request.POST.get('name', None),
            "description": request.POST.get('description', None),
            "event_date": request.POST.get('event_date', None),
            "location": request.POST.get('location', None),
        }
        form = EventForm(event_items)
        tags = request.POST.get('tags', None).split(";")
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.pub_date = timezone.localtime()
            event.save()
            event.add_tags(tags)
        context = {'form': form}
        return render(request, self.template_name, context)
    def get(self, request):
        '''Handles displaying the empty form'''
        form = EventForm()
        return render(request, self.template_name, {'form': form})
    def get_queryset(self):
        pass


class EditEvent(View):
    template_name = 'events/edit_event.html'
    model = Event
    form_class = EditEventForm

    def post(self, request, event_id):
        pass

    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        form = EditEventForm(instance=event)
        context = {'form': form, 'event': event}
        return render(request, self.template_name, context)

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        form = EditEventForm(request.POST, instance=event)
        tags = request.POST.get('tags', None).split(",")
        tags = [tag.title().strip() for tag in tags]
        tags = set(tags)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.pub_date = timezone.localtime()
            event.tags = ", ".join(tags)
            event.email = request.user.email
            event.photourl = 'https://meetup-finder-static.s3.amazonaws.com/media/images/{}'.format(event.photo.name)
            event.save()
            for user in form.cleaned_data['invitees']:
                event.invitees.add(user)
            form.save()
        context = {'form': form}
        
        subject = 'Change to Event You Signed Up For'
        message = 'Hey There!\n\n It looks like there has been a change to an event you signed up for! The event in question is: '+ event.name +'.\n\n Come see the changes at http://127.0.0.1:8000/events/'+ str(event.id) +'/. \n\n See you soon,\n Kool Katz - Event Finder Team'
        email_from = settings.EMAIL_HOST_USER
        recipients = []
        for user in event.attendees.all():
            recipients.append(user.email)
        
        send_mail(subject, message, email_from, recipients)

        # message = (
        #         'Change to Event You Signed Up For',
        #         'Hello there, there has been a change in an event you are signed up for!',
        #         'npc4crc@virginia.edu',
        #         ['npc4crc@virginia.edu'],
        # )
        # send_mass_mail((message))

        # for user in event.attendees.all() :
        #     something
        
        return redirect("/events/{}".format(event_id))

def post_detail(request, event_id):
    template_name = 'events/details.html'
    event = Event.objects.get(id=event_id)
    comments = event.comments.all()
    new_comment = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.pub_date = timezone.localtime()
            new_comment.post_id = event_id
            new_comment.save()
    else: # GET instead of POST
        form = CommentForm()
    context = {
        'event': event,
        'comments': comments,
        'new_comment': new_comment,
        'form': form,
    }
    return render(request, template_name, context)

def myEvents(request):
    '''Try except since anonymous user does not have email attribute'''
    try:
        user = User.objects.get(email=request.user.email)
        context = {
            'made': Event.objects.filter(Q(author=user)),
            'invite': Event.objects.filter(Q(invitees=user)),
            'bookmark': Event.objects.filter(Q(users_bookmarked=user)),
            'attendees': Event.objects.filter(Q(attendees=user)),
        }
    except:
        context = {
            'made': None,
            'invite': None,
            'bookmark': None,
            'attendees': None,
        }
    return render(request,'events/myEvents.html',context)

def profile(request, username):
    a = get_object_or_404(User, username=username)
    user = User.objects.get(email=request.user.email)
    context = {
        'a' : get_object_or_404(User, username=username),
        'events': Event.objects.filter(Q(author=a)&(Q(invitees__isnull=True)|Q(invitees=user))),
    }
    return render(request,'events/authorInfo.html',context)

def bookmark(request, event_id):
    '''See if user clicking bookmark is already bookmarked, if so remove, if not add'''
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    already_bookmarked = False

    for user_bookmarked in event.users_bookmarked.all() :
        if (user == user_bookmarked) :
            already_bookmarked = True
    if (already_bookmarked):
        event.users_bookmarked.remove(user.id)
    else:
        event.users_bookmarked.add(user.id)

    return redirect('/events/' + str(event_id))

def attending(request, event_id):
    '''See if user clicking to attend is already attending, if so remove, if not add'''
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    already_attending = False

    for attendee in event.attendees.all() :
        if (user == attendee) :
            already_attending = True
    if (already_attending):
        event.attendees.remove(user.id)
    else:
        event.attendees.add(user.id)

    return redirect('/events/' + str(event_id))

