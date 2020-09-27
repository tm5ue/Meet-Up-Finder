from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.list import ListView, View
from .models import Event
from .forms import EventForm

# Create your views here.
class Index(ListView):
    template_name = 'events/index.html'

    def get_queryset(self):
        pass


class AddEvent(TemplateView):
    template_name = 'events/add_event.html'

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            # event.pub_date =
            event.save()
            # name = form.cleaned_data.get('name')
            # description = form.cleaned_data.get('description')
            # event = Event.objects.create(name=name, description=description)
            # event.save()

        context = {'form': form}
        return render(request, self.template_name, context)


    def get(self, request):
        form = EventForm()
        return render(request, self.template_name, {'form': form})


    def get_queryset(self):
        pass