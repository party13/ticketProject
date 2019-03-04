from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [
    path('', add_comment, name='add_ticket_comment'),

]