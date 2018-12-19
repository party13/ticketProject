from django.urls import path
from .views import *



urlpatterns = [
    path('', index_page, name='index_page'),
    path('news/', tickets_list),
    path('ticket/<str:number>/', TicketDetail.as_view(), name='ticket_detail_url')


]