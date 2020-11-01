
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import LogoutView, LoginView

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    url('^soc/', include('social_django.urls', namespace='social')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(template_name='events/index.html'), name='logout'),
    
    path('events/add', views.AddEvent.as_view(), name='add_event'),
    path('events/<int:event_id>/', views.post_detail, name='detail'),
    path('events/<int:event_id>/bookmark', views.bookmark),
    path('events/<int:event_id>/attending', views.attending),
    
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('events/<int:event_id>/edit_event', views.EditEvent.as_view(), name='edit_event'),
    path('user/<str:username>/', views.profile, name='authorDetail'),
   
    path('events/myEvents', views.myEvents, name='myEvents'),
]
