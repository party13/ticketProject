from django.urls import path, include
from django.conf.urls import  url
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [
    url(r'term/request/(?P<number>\d+)$', TermRequest.as_view(), name='term_request'),
    url('term/confirm/(?P<number>\d+)$', TermConfirm.as_view(), name='confirm_term_change'),
# url('ticket/delete/(?P<number>\d+)$', DeleteTicket.as_view(), name='delete_ticket'),

]