from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView, View
from django.utils import timezone
from .models import Event, Tag, EventTag, Comment
from .forms import EventForm, inviteForm, CommentForm, EditEventForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_datepicker_plus import DateTimePickerInput
from django import template

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

class SearchResultsView(ListView):
    model = Event
    template_name = 'events/search_results.html'
    def get_queryset(self):
        '''Get search criteria and return list of corresponding events'''
        query = self.request.GET.get('q')
        user = User.objects.get(email=self.request.user.email)
        event_list = Event.objects.filter(
            (Q(invitees__isnull=True)|Q(invitees=user)|Q(author=user))&
            #either public/invited events/events you wrote
            (Q(name__icontains=query) |
            Q(eventtag__in=EventTag.objects.filter(t__icontains=query)))
        ).distinct()
        return event_list
    # TODO: modify search for multiple keywords
    # TODO: add filtering

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
        tags = request.POST.get('tags', None).split(";").strip()
        tags = [tag.title().strip() for tag in tags]
        tags = set(tags)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.pub_date = timezone.localtime()
            event.tags = ", ".join(tags)
            event.save()
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
        context = {'form': form}
        return render(request, self.template_name, context)\

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        form = EditEventForm(request.POST, instance=event)
        if form.is_valid(): pass

class EventTime(CreateView):
    '''For inputting in the datetime field in the form'''
    model = Event
    form_class = EventForm


def post_detail(request, event_id):
    template_name = 'events/details.html'

    event = Event.objects.get(id=event_id)
    comments = event.comments.all()
    new_comment = None
    if request.method == 'POST':
        comment_items = {
            "name": request.POST.get('name'),
            "description": request.POST.get('description'),
        }
        form = CommentForm(comment_items)
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

class inviteEvent(TemplateView):
    form_class=inviteForm
    template_name = 'events/invite.html'

    def get(self, request):
        '''Handles displaying the empty form'''
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        '''Handles adding a new event'''
        form = inviteForm(request.POST)

        tags = request.POST.get('tags', None).split(";").strip()
        tags = [tag.title().strip() for tag in tags]
        tags = set(tags)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.pub_date = timezone.localtime()
            event.tags = ", ".join(tags)
            event.save()
            for user in form.cleaned_data['invitees']:
                event.invitees.add(user)
        context = {'form': form}
        return render(request, self.template_name, context)

register = template.Library()

def myEvents(request):
    '''Try except since anonymous user does not have email attribute'''
    try:
        user = User.objects.get(email=request.user.email)
        context = {
            'made': Event.objects.filter(Q(author=user)),
            'invite': Event.objects.filter(Q(invitees=user)),
        }
    except:
        context = {
            'made': None,
            'invite': None,
        }
    return render(request,'events/myEvents.html',context)
    
class UserView(generic.ListView):
    model= User
    template_name = 'events/invite.html'
    def get_queryset(self):
        return User.objects.all()
