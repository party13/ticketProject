from django.urls import path, include
from django.conf.urls import  url
from django.contrib.auth import views as auth_views
from .views import *




urlpatterns = [
    # path('', MyTickets.as_view(), name='index_page'),

    path('sign', signer_sign, name='signer_sign'),


    # url(r'^jsi18n/$', null_javascript_catalog, name='javascript_catalog'),
]