# mini_insta/urls.py
# Gracious Ogyiri Asare- gpoa@bu.edu

from django.urls import path
from django.views.generic import TemplateView
from . import views 
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # URL patterns for the voter_analytics app
    path('', views.VoterListView.as_view(), name='home'),
    path('results', views.VoterListView.as_view(), name='voters_list'),
    path('voter/<int:pk>', views.ResultDetailView.as_view(), name='voter'),
    path('graphs', views.GraphsView.as_view(), name='graphs'),
]