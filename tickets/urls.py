from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [
    path('', index_page, name='index_page'),
    path('search/', search_results, name='search_results_url'),
    path('news/', TicketsList.as_view(), name='news_list' ),
    path('ticket/create/', CreateTicket.as_view(), name='create_ticket'),
    path('ticket/sign_ticket/', sign_ticket, name='sign_ticket'),
    path('ticket/<str:number>/', TicketDetail.as_view(), name='ticket_detail_url'),
    path('plan/', TicketPlan.as_view() ),

]