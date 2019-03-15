from django.urls import path, include
from django.conf.urls import  url
from django.contrib.auth import views as auth_views
from .views import *


from django.views.i18n import null_javascript_catalog


urlpatterns = [
    path('', MyTickets.as_view(), name='index_page'),
    path('search/', search_results, name='search_results_url'),
    path('all/', MyTickets.as_view(), name='all' ),
    path('all/plan<str:days>/', PlannedTickets.as_view(), name='my_plan' ),
    path('my/plan<str:days>/', PlannedTickets.as_view(), name='my_departments_plan' ),
    path('my/', MyDepartmentTickets.as_view(), name='my_department_tickets' ),
    path('news/', NewTickets.as_view(), name='news' ),
    path('ticket/archive/', ArchivedTickets.as_view(), name='archive'),
    path('ticket/create/', CreateTicket.as_view(), name='create_ticket'),
    path('report/', ReportedTickets.as_view(), name= 'my_report' ),
    url('ticket/copy/(?P<number>\d+)$', CreateTicket.as_view(), name='copy'),
    url('ticket/delete/(?P<number>\d+)$', DeleteTicket.as_view(), name='delete_ticket'),
    url('ticket/reject/(?P<number>\d+)$', RejectTicket.as_view(), name='reject_ticket'),
    url('ticket/redirect/(?P<number>\d+)$', RedirectTicket.as_view(), name='redirect_ticket'),
    url('ticket/edit/(?P<number>\d+)$', EditTicket.as_view(), name='edit_ticket'),
    path('ticket/sign_ticket/', sign_ticket, name='sign_ticket'),
    path('ticket/make_reports/', make_reports, name='make_reports'),
    path('ticket/<str:number>/', TicketDetail.as_view(), name='ticket_detail_url'),

    url(r'^jsi18n/$', null_javascript_catalog, name='javascript_catalog'),
]