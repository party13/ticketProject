# Create your views here.
#
# from django.contrib import sessions
# from django.forms import ModelMultipleChoiceField
# from django.http import HttpResponse
# from KB_Users.models import UserKB


from django.shortcuts import render, redirect
from .models import Ticket, News
from .forms import CreateTicketForm
from .utils import generate_number, user_dept
from django.views.generic import View
from django.db.models import Q
from datetime import date, timedelta
from django.core.paginator import Paginator

tickets_global = Ticket.objects.all().exclude(status__exact='closed')       # to be changed later
themes = set(Ticket.objects.values_list('theme', flat=True))
newNumber = generate_number()

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
            searched_themes=set(tickets.values_list('theme', flat=True))
            total = str(total)
            if total[-1] in '567890' or total in ['11','12','13','14']:
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
    username = request.user or None
    ticket_number = request.POST.get('tn', '') or None
    #us_id = request.session.get('_auth_user_id')
    #username = UserKB.objects.get(id=us_id)
    if username and ticket_number:
        ticket_query = Ticket.objects.filter(number=ticket_number)
        ticket = ticket_query.first()
        if ticket.responsible == username:
            ticket_query.update(isSignedByResponsible=True)
            new = News(responsibleID=ticket.consumer.id, ticketNumber=ticket.id)
            new.save()
            print('signed by resp')
        if ticket.consumer == username:
            ticket_query.update(isSignedByCustomer = True)
            ticket.refresh_from_db()
            print('signed by consum')
            print('checking ticket for closing-?')
            if ticket.mayBeClosed():
                print('ok. closing ticket')
                # можно закрыть карточку
                ticket.closeTicket()

        return redirect(ticket)

def make_reports(request):
    comments = request.POST.get('report_comments', '') or None
    ticket_number = request.POST.get('tn', '') or None
    ticket_q = Ticket.objects.filter(number=ticket_number)
    ticket_q.update(reports=comments)
    # ticket.save()
    return redirect(ticket_q.first())


class TicketsList(View):
    def get(self, request):
        username, dept_number, updates = user_dept(request)
        theme_filter = request.GET.get('theme', '')
        if theme_filter:
            tickets = Ticket.objects.filter(theme__iexact=theme_filter)
        else:
            tickets = tickets_global

        paginator = Paginator(tickets, 15)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
        next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''


        context = {'tickets': tickets,
                   'updates': updates,
                   'user_name': username,
                   'themes': themes,
                   'dept_number' : dept_number,
                   'page_object': page,
                   'is_paginated': is_paginated,
                   'next_url': next_url,
                   'prev_url': prev_url
                   }

        return render(request, 'tickets/index.html', context=context)
    # def post(self, request, theme):
    #     return render(request, 'tickets/index.html', context={})


class NewTickets(View):
    def get(self, request):
        username, dept_number, _ = user_dept(request)
        if request.user.is_authenticated:
            news = News.objects.filter(responsibleID__exact=username.id).values_list('ticketNumber', flat=True)
            tickets= Ticket.objects.filter(id__in=news)
            updates = len(news)

        context = {'tickets': tickets,
                   'updates': updates,
                   'user_name': username,
                   'themes': themes,
                   'dept_number' : dept_number,
                   }

        return render(request, 'tickets/index.html', context=context)


class TicketDetail(View):
    def get(self, request, number):
        username, dept_number, updates = user_dept(request)
        ticket = Ticket.objects.get(number__iexact=number)
        news = News.objects.filter(Q(responsibleID = request.session.get('_auth_user_id')) &
                                   Q(ticketNumber = ticket.id))
        # удаляем "новости"
        ticketIsNew = len(news) > 0
        news.delete()

        context= {'ticket':ticket,
                  'user_name': username,
                  'themes': themes,
                  'dept_number': dept_number,
                  'ticketIsNew': ticketIsNew,
                  'updates': updates
                  }
        return render(request, 'tickets/ticket_detail.html', context = context)

    def post(self, request):
        return render(request, 'tickets/index.html', context={})


class TicketPlan(View):
    def get(self, request):
        username, dept_number, updates = user_dept(request)
        days = request.GET.get('plan', '')
        td = date.today()
        planned_ticket = tickets_global.filter(term__range=(td, td + timedelta(int(days))))
        planned_ticket = planned_ticket.filter(Q(responsible=username) | Q(consumer=username))


        context = {'tickets': planned_ticket,
                   'user_name': username,
                   'days' : days,
                   'themes': themes,
                   'updates': updates,
                   'dept_number': dept_number
                   }
        return render(request, 'tickets/plan.html', context=context)


class CreateTicket(View):
    template = 'tickets/ticket_create_form.html'
    def get(self, request):
        user = request.user
        form = CreateTicketForm (user)


        return render( request, self.template, context={'form': form,
                                                        'user_name': user,
                                                        'dept_number': request.user.department,
                                                        'themes' : themes})

    def post(self, request):
        user = request.user
        form = CreateTicketForm(user, request.POST or None)
        data = form.data
        print(data)

        if form.is_valid():
            data = form.cleaned_data
            print('valid data', data)
            new_ticket = form.save(commit=False)
            new_ticket.consumer = user
            new_ticket.osn = 'Поручение от {}'.format(user)
            nmbr = next(newNumber)
            new_ticket.number = nmbr
            new_ticket.save()
            # message = ''
            # message = 'Карточка создана, номер: '.format(new_ticket.number)
            return redirect(new_ticket)

        return render(request, self.template, context={'form': form})



class Archive(View):
    def get(self, request):
        username, dept_number, updates = user_dept(request)
        archive_tickets =  Ticket.objects.filter( Q(consumer=username) | Q(responsible=username))
        archive_tickets = archive_tickets.filter(Q(status='closed') )
        context = {'tickets': archive_tickets,
                   'user_name': username,
                   'themes': themes,
                   'updates': updates,
                   'dept_number': dept_number
                   }

        return render(request, 'tickets/archive.html', context=context)

    def post(self, request):
        pass


class Report (View):
    def get(self, request):
        username, dept_number, updates = user_dept(request)
        days = request.GET.get('report', '') or None
        td = date.today()
        reported_tickets = tickets_global.filter(Q(term__range=(td - timedelta(int(days)), td )) & Q(status='closed') & Q(consumer=username)) # to be changed later
        context = {'tickets': reported_tickets,
                   'user_name': username,
                   'days': days,
                   'themes': themes,
                   'updates': updates,
                   'dept_number': dept_number
                   }
        return render(request, 'tickets/report.html', context=context)

    def post(self, request):
        return