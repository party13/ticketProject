from django.urls import path, include
from django.conf.urls import  url

from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [
    path('', add_comment, name='add_ticket_comment'),
    path('comments/', all_comments, name='all_comments'),
    url('comments/delete/(?P<id>\d+)$', delete_comment, name='delete_comment'),

]