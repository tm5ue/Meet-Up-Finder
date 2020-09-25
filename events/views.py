from django.shortcuts import render
from django.views import generic
from django.views.generic.list import ListView

# Create your views here.
class Index(ListView):
    template_name = 'events/index.html'

    def get_queryset(self):
        pass


class AddEvent(ListView):
    pass
    # TODO: