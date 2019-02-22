from django.urls import path, include
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [
    path('', TicketsList.as_view(), name='index_page'),
    path('search/', search_results, name='search_results_url'),
    path('all/', TicketsList.as_view(), name='all' ),
    path('news/', NewTickets.as_view(), name='news' ),
    path('ticket/create/', CreateTicket.as_view(), name='create_ticket'),
    url('ticket/copy/(?P<number>\d+)$', CreateTicket.as_view(), name='copy'),
    url('ticket/delete/(?P<number>\d+)$', DeleteTicket.as_view(), name='delete_ticket'),
    url('ticket/edit/(?P<number>\d+)$', EditTicket.as_view(), name='edit_ticket'),
    path('ticket/archive/', Archive.as_view(), name='archive'),
    path('ticket/sign_ticket/', sign_ticket, name='sign_ticket'),
    # url(r'comments/(?:page-(?P<page_number>\d+)/)?$', comments),
    path('ticket/make_reports/', make_reports, name='make_reports'),

    path('ticket/<str:number>/', TicketDetail.as_view(), name='ticket_detail_url'),
    path('share/', share_ticket, name='share'),
    # path('copy/', copy_ticket, name='copy'),
    path('plan/', TicketPlan.as_view() ),
    path('report/', Report.as_view() ),
]