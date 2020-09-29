from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView, View
from django.utils import timezone
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
class Index(ListView):
    '''Class for home page'''
    template_name = 'events/index.html'

    def get_queryset(self):
        '''
        Get all Events to display on home page
        :return:
        '''
        return Event.objects.all()


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
            # name = form.cleaned_data.get('name')
            # description = form.cleaned_data.get('description')
            # event = Event.objects.create(name=name, description=description)
            # event.save()

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
    
#    def user_is_not_logged_in(user):
#        return not user.is_authenticated()
#    @user_passes_test(user_is_not_logged_in)
    def get(self, request, event_id):
        '''Queries database for an event based on event_id parameter, returns page with details'''
        event = Event.objects.get(id=event_id)
        context = {'event': event}
        print(context)
        return render(request, self.template_name, context)
     
    
