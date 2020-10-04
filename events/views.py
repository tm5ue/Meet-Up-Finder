from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView, View
from django.utils import timezone
from .models import Event
from .forms import EventForm, inviteForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
class Index(ListView):
    '''Class for home page'''
    template_name = 'events/index.html'
    Model=Event
    def get_queryset(self):
        '''
        Get all Events to display on home page
        :return:
        '''
        return Event.objects.filter(Q(friends= '')|Q(friends__isnull=True)) #public events
        #(~Q(friends="")|Q(friends=""))
class AddEvent(TemplateView):
    template_name = 'events/add_event.html'
    def post(self, request):
        '''Handles adding a new event'''
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.pub_date = timezone.localtime()
            event.save()
        context = {'form': form}
        return render(request, self.template_name, context)
    def get(self, request):
        '''Handles displaying the empty form'''
        form = EventForm()
        return render(request, self.template_name, {'form': form})
    def get_queryset(self):
        pass
class EventTime(CreateView):
    '''For inputting in the datetime field in the form'''
    model = Event
    form_class = EventForm
class Detail(View):
    template_name = 'events/details.html'
    def get(self, request, event_id):
        '''Queries database for an event based on event_id parameter, returns page with details'''
        event = Event.objects.get(id=event_id)
        context = {'event': event}
        print(context)
        return render(request, self.template_name, context)
class inviteEvent(TemplateView):
    form_class=inviteForm
    template_name = 'events/invite.html'
    #initial = {User.objects.all(): user.email}
    #context_object_name = 'objectList'
    def get(self, request):
        '''Handles displaying the empty form'''
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        '''Handles adding a new event'''
        form = inviteForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.pub_date = timezone.localtime()
            event.save()
            for user in form.cleaned_data['users']:
                event.users.add(user)
        context = {'form': form}
        return render(request, self.template_name, context)
#    def get_context_data(self, **kwargs):
#        context = super(inviteEvent, self).get_context_data(**kwargs)
#        # here's the difference:
#        context['objectList'] = User.objects.all()
#        print(context['objectList'])
#        return context
     
#    def get_queryset(self):
#        return User.objects.all()
        
        
#class inviteEvent(CreateView):
#    model = Event
#    fields = ['name', 'description', 'event_date','friends']
        
class MyEventsView(generic.ListView):
    template_name = 'events/myEvents.html'
    def get_queryset(self):
        user = User.objects.get(email=self.request.user.email)
        return Event.objects.filter(Q(author=user))
        #public and private events that you wrote
class UserView(generic.ListView):
    model= User
    template_name = 'events/invite.html'
    def get_queryset(self):
        return User.objects.all()
    
