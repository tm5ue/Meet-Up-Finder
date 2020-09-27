
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    url('^soc/', include('social_django.urls', namespace='social')),
    path('login/', LogoutView.as_view(template_name="events/index.html"), name='logout'),

    path('events/add', views.AddEvent.as_view(), name='add_event'),

]
