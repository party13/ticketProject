# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import sessions

from KB_Users.models import UserKB
from .models import Ticket, News
from .forms import CreateTicketForm

from django.views.generic import View
from django.db.models import Q
from datetime import date, timedelta

from django.http import HttpResponse


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
                   'text_result' : text_result,
                   'user_name': request.user,
                   'dept_number' : request.user.department
                   }
        return render(request, 'tickets/search_results.html', context = context)
    else:
        return render(request, 'tickets/index.html')


def sign_ticket(request):
    print ('подписание...')
    username = request.user or None
    ticket_number = request.POST.get('tn', '') or None
    #us_id = request.session.get('_auth_user_id')
    #username = UserKB.objects.get(id=us_id)
    if username and ticket_number:
        ticket_query = Ticket.objects.filter(number = ticket_number)
        ticket = ticket_query.first()
        if ticket.responsible == username:
            ticket_query.update(isSignedByResponsible = True)
        if ticket.consumer == username:
            ticket_query.update(isSignedByCustomer = True)
            print('checking ticket for closing-?')
            if ticket.mayBeClosed():
                print('ok. closing ticket')
                # можно закрыть карточку
                ticket.closeTicket()

        return redirect(ticket)
    print ('yt elfkjcm gjlgbcfnm')

def make_reports(request):
    comments = request.POST.get('report_comments', '') or None
    ticket_number = request.POST.get('tn', '') or None
    ticket_query = Ticket.objects.filter(number=ticket_number)
    ticket = ticket_query.first()
    print(comments)
    print(ticket)
    ticket_query.update(reports=comments)

    return redirect(ticket)



tickets_global = Ticket.objects.all()
tickets_global = tickets_global.exclude(status__exact='closed')
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

        # themes = []
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


class NewTickets(View):
    def get(self, request):
        updates = 0
        username = None
        dept_number = ''
        if request.user.is_authenticated:
            username = request.user
            news = News.objects.filter(responsibleID__exact=username.id).values_list('ticketNumber', flat=True)

            tickets= Ticket.objects.filter(id__in=news)
            updates = len(news)
            dept_number = username.department

        context = {'tickets': tickets,
                   'updates': updates,
                   'user_name': username,
                   'themes': themes,
                   'dept_number' : dept_number
                   }

        return render(request, 'tickets/index.html', context=context)


class TicketDetail(View):
    def get(self, request, number):
        #ticket = get_object_or_404(Ticket, number__iexact=number)


        if request.user.is_authenticated:
            username = request.user
        else:
            username = None

        ticket = Ticket.objects.get(number__iexact=number)
        try:
            updates = News.objects.filter(responsibleID__exact=username.id).count()
        except:
            updates = 0

        #  Ok, news- 20 ticket.id-  17  responsible ID-  4
        #         ticket.isRead = True
        ticketIsNew = False
        news = News.objects.filter(Q(responsibleID = request.session.get('_auth_user_id')) &
                                   Q(ticketNumber = ticket.id))
        # удаляем "новости"
        ticketIsNew = len(news) > 0
        news.delete()

        context= {'ticket':ticket,
                  'user_name': username,
                  'themes': themes,
                  'dept_number': username.department,
                  'ticketIsNew': ticketIsNew,
                  'updates': updates
                  }
        return render(request, 'tickets/ticket_detail.html', context = context)

    def post(self, request):
        return render(request, 'tickets/index.html', context={})


class TicketPlan(View):
    def get(self, request):
        days = request.GET.get('plan', '')
        if request.user.is_authenticated:
            username = request.user
        else:
            username = None

        td = date.today()
        planned_ticket = tickets_global.filter(term__range=(td, td + timedelta(int(days))))
        planned_ticket = planned_ticket.filter(Q(responsible=username) | Q(consumer=username))

        try:
            updates = News.objects.filter(responsibleID__exact=username.id).count()
        except:
            updates = 0

        context = {'tickets': planned_ticket,
                   'user_name': username,
                   'days' : days,
                   'themes': themes,
                   'updates': updates,
                   'dept_number': username.department
                   }
        return render(request, 'tickets/plan.html', context=context)


class CreateTicket(View):
    template = 'tickets/ticket_create_form.html'
    def get(self, request):
        form = CreateTicketForm ()

        return render( request, self.template, context={'form': form,
                                                        'user_name': request.user,
                                                        'dept_number': request.user.department,
                                                        'themes':themes})

    def post(self, request):
        form = CreateTicketForm(request.POST)
        user = request.user
        if form.is_valid():
            data = form.cleaned_data
            print('valid')
            new_ticket = form.save(commit=False)
            new_ticket.consumer = user
            new_ticket.osn = 'Поручение от {}'.format(user)

            new_ticket.save()
            message = ''
            #message = 'Карточка создана, номер: '.format(new_ticket.number)
            return redirect(new_ticket)

        return render(request, self.template, context={'form': form})



class Archive(View):
    def get(self, request):
        username = request.user or None
        archive_tickets = Ticket.objects.filter(status__exact='closed')

        try:
            updates = News.objects.filter(responsibleID__exact=username.id).count()
        except:
            updates = 0

        context = {'tickets': archive_tickets,
                   'user_name': username,
                   'themes': themes,
                   'updates': updates,
                   'dept_number': username.department

                   }

        return render(request, 'tickets/archive.html', context=context)

    def post(self, request):
        pass