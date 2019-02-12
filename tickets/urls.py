from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [
    path('', index_page, name='index_page'),
    path('search/', search_results, name='search_results_url'),
    path('all/', TicketsList.as_view(), name='all' ),
    path('news/', NewTickets.as_view(), name='news' ),
    path('ticket/create/', CreateTicket.as_view(), name='create_ticket'),
    path('ticket/archive/', Archive.as_view(), name='archive'),
    path('ticket/sign_ticket/', sign_ticket, name='sign_ticket'),
    path('ticket/make_reports/', make_reports, name='make_reports'),

    path('ticket/<str:number>/', TicketDetail.as_view(), name='ticket_detail_url'),
    path('plan/', TicketPlan.as_view() ),
    path('report/', Report.as_view() ),
]