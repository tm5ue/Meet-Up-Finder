from django.urls import path

from . import views

app_name = 'maps'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('comments/', views.comments, name='comments'),
    # path('comments/list', views.comments_list, name='comments_list'),

]