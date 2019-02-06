# Create your views here.
from django.shortcuts import render, redirect
from .models import Ticket, News
from django.views.generic import View
from django.db.models import Q
from datetime import date, timedelta


def index_page(request):
    if request.user.is_authenticated:
        userlogin = request.user
        news_quantity = News.objects.filter(responsibleID__exact=userlogin.id).count()
    else:
        userlogin =  '@#(*%^()@()@T&#ttgaz23g -- no user --- @#(*%^()@()@T&#ttgaz23g '
        news_quantity = ''
    context = {
        'user_login' : userlogin,
        'count' : news_quantity
    }
    return render(request, 'tickets/index.html', context = context)


def search_results(request):
    search_query = request.GET.get('search', '')
    search_query.strip()
    if search_query != "":
        tickets = Ticket.objects.filter(
            Q(job__icontains = search_query) |
            #Q(number = str(search_query) ) |
            Q(theme__istartswith = search_query)
        )
        total = len(tickets)
        searched_themes=[]
        text_result=''
        if total>0:

            for ticket in tickets:
                if ticket.theme not in searched_themes:
                    searched_themes.append(ticket.theme)
            total = str(total)
            if total[-1] in '567890':
                text_result = 'Найдено {} карточек'.format(total)
            elif total[-1] in '234':
                text_result = 'Найдено {} карточки'.format(total)
            else:
                text_result= 'Найдена {} карточка'.format(total)


        context = {'tickets': tickets,
                   'themes': searched_themes,
                   'search_text': search_query,
                   'text_result' : text_result
                   }
        return render(request, 'tickets/search_results.html', context = context)
    else:
        return render(request, 'tickets/index.html')


tickets_global = Ticket.objects.all()
themes=[]
for ticket in tickets_global:
    if ticket.theme not in themes:
        themes.append(ticket.theme)


class TicketsList(View):
    def get(self, request):
        updates = 0
        username = None
        dept_number = ''
        if request.user.is_authenticated:
            username = request.user
            updates = News.objects.filter(responsibleID__exact=username.id).count()
            dept_number = username.department

        themes = []
        theme_filter = request.GET.get('theme', '')

        if theme_filter:
            tickets = Ticket.objects.filter(theme__iexact=theme_filter)
        else:
            tickets = tickets_global

        context = {'tickets': tickets,
                   'updates': updates,
                   'user_name': username,
                   'themes': themes,
                   'dept_number' : dept_number
                   }

        return render(request, 'tickets/index.html', context=context)

    def post(self, request, theme):
        return render(request, 'tickets/index.html', context={})


class TicketDetail(View):

    def get(self, request, number):
        #ticket = get_object_or_404(Ticket, number__iexact=number)

        if request.user.is_authenticated:
            username = request.user
            print(request.user)
        else:
            username = None

        ticket = Ticket.objects.get(number__iexact=number)
        #ticket.isRead = True
        context= {'ticket':ticket,
                  'user_name': username,
                  'themes': themes
                  }
        return render(request, 'tickets/ticket_detail.html', context = context)


class TicketPlan(View):

    def get(self, request):
        days = request.GET.get('plan', '')
        if request.user.is_authenticated:
            username = request.user
        else:
            username = None

        td = date.today()
        planned_ticket = tickets_global.filter(term__range=(td, td + timedelta(int(days))))
        context = {'tickets': planned_ticket,
                   'user_name': username,
                   'days' : days
                   }

        return render(request, 'tickets/plan.html', context=context)
