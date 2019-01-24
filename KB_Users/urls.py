from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [
    path('', Cabinet.as_view(), name='cabinet'),
    path('login/', MyLogin.as_view(), name='login_url'),
    path('logout/', logout_view, name='logout'),
    path('password-change/', MyChangePassword.as_view(), name='password_change'),
    path('password-reset/', MyResetPassword.as_view(), name='password_reset')
]