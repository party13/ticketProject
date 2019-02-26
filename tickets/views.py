# Create your views here.
#
from django.contrib import sessions
# from django.forms import ModelMultipleChoiceField
# from django.http import HttpResponse
# from KB_Users.models import UserKB
from django.shortcuts import render, redirect, reverse
from .models import Ticket, News
from .forms import CreateTicketForm
from .utils import *
from django.views.generic import View
from django.db.models import Q
from datetime import date, timedelta
from django.core.paginator import Paginator

tickets_global = Ticket.objects.all().exclude(status__exact='closed')       # to be changed later
themes = set(tickets_global.values_list('theme', flat=True))                # to be changed later
newNumber = generate_number()


def search_results(request):
    username, dept_number, updates = user_dept(request)
    search_query = request.GET.get('search', '').strip()
    if search_query != "":
        if search_query.isdigit():
            tickets = Ticket.objects.filter(number__contains=search_query)
        else:
            tickets = Ticket.objects.filter(job__icontains = search_query)
        total = len(tickets)
        searched_themes=[]
        text_result=''
        if total>0:
            searched_themes=set(tickets.values_list('theme', flat=True))
            text_result = 'Найдено' + found_ticket_text(total)
            # total = str(total)
        paginator = Paginator(tickets, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.page(page_number)
        is_paginated = page.has_other_pages()
        prev_url = '?search={}&page={}'.format( search_query, page.previous_page_number()) if page.has_previous() else ''
        next_url = '?search={}&page={}'.format(search_query, page.next_page_number()) if page.has_next() else ''

        context = {'tickets': tickets,
                   'themes': searched_themes,
                   'search_text': search_query,
                   'text_result' : text_result,
                   'user_name': username,
                   'dept_number' : dept_number,
                   'page_object': page,
                   'is_paginated': is_paginated,
                   'next_url': next_url,
                   'prev_url': prev_url,
                   }
        return render(request, 'tickets/search_results.html', context = context)
    else:
        return render(request, 'tickets/index.html')


def sign_ticket(request):
    username = request.user or None
    ticket_number = request.POST.get('tn', '') or None
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


def share_ticket(request):
    # username = request.user or None
    number = request.GET.get('number', '')
    ticket = Ticket.objects.get(number=number)

    print('sharing...')
    url = number
    print(ticket)

    return redirect(ticket)


class TicketsList(View):
    def get(self, request):
        username, dept_number, updates = user_dept(request)
        theme_filter = request.GET.get('theme', '')

        # !!!! this logic to be fixed later what tickets to show
        tickets = tickets_global.filter(Q(responsible=username) |
                                        Q(consumer=username)).exclude(status='closed')
        if theme_filter:
            tickets = tickets.filter(theme__iexact=theme_filter)

        text_result = found_ticket_text(len(tickets))
        paginator = Paginator(tickets, 15)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
        next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''


        context = {'tickets': tickets,
                   'text_result': text_result,
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
            text_result = found_ticket_text(len(tickets))
            updates = len(news)

        paginator = Paginator(tickets, 15)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
        next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''

        context = {'tickets': tickets,
                   'text_result':text_result,
                   'updates': updates,
                   'user_name': username,
                   'themes': themes,
                   'dept_number': dept_number,
                   'page_object': page,
                   'is_paginated': is_paginated,
                   'next_url': next_url,
                   'prev_url': prev_url
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


class CreateTicket(View):
    template = 'tickets/ticket_create_form.html'
    instance = None

    def get(self, request, number=None):
        if number:
            self.instance = Ticket.objects.get(number=number)
        user = request.user
        form = CreateTicketForm (user, instance=self.instance)

        return render( request, self.template, context={'form': form,
                                                        'user_name': user,
                                                        'dept_number': request.user.department,
                                                        'themes' : themes})

    def post(self, request):
        user = request.user
        form = CreateTicketForm(user, request.POST or None)

        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.consumer = user
            new_ticket.osn = 'Поручение от {}'.format(user)

            while not new_ticket.id:
                try:
                    nmbr = next(newNumber)
                    new_ticket.number = nmbr
                    new_ticket.save()
                except:
                    nmbr = next(newNumber)
            return redirect(new_ticket)

        return render(request, self.template, context={'form': form,
                                                        'user_name': user,
                                                        'dept_number': request.user.department,
                                                        })


class EditTicket(View):
    template = 'tickets/ticket_edit_form.html'
    def get(self, request, number):
        instance = Ticket.objects.get(number=number)
        user = request.user
        form = CreateTicketForm(user, instance=instance)

        return render(request, self.template, context={'form': form,
                                                       'user_name': user,
                                                       'dept_number': request.user.department,
                                                       'ticket' : instance
                                                       })

    def post(self, request, number):
        user = request.user
        instance = Ticket.objects.get(number=number)
        form = CreateTicketForm(user, request.POST, instance=instance)

        if form.is_valid():
            new_ticket = form.save()
            return redirect(new_ticket)

        # form.errors
        print('not valid form')

        return render(request, self.template, context={'form': form,
                                                        'user_name': user,
                                                        'dept_number': request.user.department,
                                                        'ticket': instance
                                                        })


class DeleteTicket(View):
    def get(self, request, number):
        username, dept_number, updates = user_dept(request)
        ticket = Ticket.objects.get(number__iexact=number)

        context= {'ticket':ticket,
                  'user_name': username,
                  'themes': themes,
                  'dept_number': dept_number,
                  'updates': updates
                  }
        return render(request, 'tickets/delete_ticket.html', context = context)

    def post(self, request, number):
        ticket = Ticket.objects.get(number__iexact=number)
        ticket.delete()
        return redirect(reverse('all'))


class Archive(View):
    def get(self, request):
        username, dept_number, updates = user_dept(request)
        archive_tickets =  Ticket.objects.filter( Q(consumer=username) | Q(responsible=username))
        archive_tickets = archive_tickets.filter(Q(status='closed') )

        paginator = Paginator(archive_tickets, 15)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
        next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''

        text_result = found_ticket_text(len(archive_tickets))

        context = {'tickets': archive_tickets,
                   'text_result':text_result,
                   'updates': updates,
                   'user_name': username,
                   'themes': themes,
                   'dept_number': dept_number,
                   'page_object': page,
                   'is_paginated': is_paginated,
                   'next_url': next_url,
                   'prev_url': prev_url
                   }

        return render(request, 'tickets/archive.html', context=context)

    def post(self, request):
        pass


class TicketPlan(View):
    def get(self, request):
        username, dept_number, updates = user_dept(request)
        days = request.GET.get('plan', '')
        td = date.today()
        planned_ticket = tickets_global.filter(term__range=(td, td + timedelta(int(days))))
        planned_ticket = planned_ticket.filter(Q(responsible=username) | Q(consumer=username))
        text_result = found_ticket_text(len(planned_ticket))

        paginator = Paginator(planned_ticket, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        prev_url = '?plan={}&page={}'.format(days, page.previous_page_number()) if page.has_previous() else ''
        next_url = '?plan={}&page={}'.format(days, page.next_page_number()) if page.has_next() else ''

        context = {'tickets': planned_ticket,
                   'text_result':text_result,
                   'updates': updates,
                   'user_name': username,
                   'themes': themes,
                   'days': days,
                   'dept_number': dept_number,
                   'page_object': page,
                   'is_paginated': is_paginated,
                   'next_url': next_url,
                   'prev_url': prev_url
                   }
        return render(request, 'tickets/plan.html', context=context)


class Report (View):
    def get(self, request):
        username, dept_number, updates = user_dept(request)
        days = request.GET.get('report', '') or None
        td = date.today()
        reported_tickets = tickets_global.filter(Q(term__range=(td - timedelta(int(days)), td )) & Q(status='closed') & Q(consumer=username)) # to be changed later

        text_result= found_ticket_text(len(reported_tickets))

        paginator = Paginator(reported_tickets, 15)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
        next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''

        context = {'tickets': reported_tickets,
                   'text_result':text_result,
                   'updates': updates,
                   'user_name': username,
                   'themes': themes,
                   'days' : days,
                   'dept_number': dept_number,
                   'page_object': page,
                   'is_paginated': is_paginated,
                   'next_url': next_url,
                   'prev_url': prev_url,

                   }
        return render(request, 'tickets/report.html', context=context)

    def post(self, request):
        return