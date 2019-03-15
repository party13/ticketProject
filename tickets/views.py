# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
# from .models import Ticket, News
from .forms import CreateTicketForm, RedirectTicketForm
from .utils import *
from django.views.generic import View
from django.db.models import Q
from datetime import date, timedelta
from django.core.paginator import Paginator

newNumber = generate_number()

def search_results(request):
    context = initial(request)
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

        context['tickets'] = tickets
        context['themes'] = searched_themes
        context['search_text'] = search_query
        context['text_result'] = text_result

        paginator = Paginator(tickets, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.page(page_number)
        is_paginated = page.has_other_pages()
        prev_url = '?page={}&search={}'.format(page.previous_page_number(), search_query) if page.has_previous() else ''
        next_url = '?page={}&search={}'.format(page.next_page_number(), search_query) if page.has_next() else ''
        context['page_object'] = page
        context['is_paginated'] = is_paginated
        context['prev_url'] = prev_url
        context['next_url'] = next_url


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


class MyTickets(View):
    def get(self, request):
        context = initial(request)
        tickets = context.get('tickets')

        theme_filter = request.GET.get('theme', '')
        user_filter = request.GET.get('user', '')
        if theme_filter:
            tickets = tickets.filter(theme=theme_filter)
        if user_filter:
            tickets = tickets.filter(responsible=user_filter)
        if tickets:
            text_result = found_ticket_text(len(tickets))
            context['text_result'] = text_result
            context = paginate_tickets(request, tickets, context)
        return render(request, 'tickets/index.html', context=context)


class MyDepartmentTickets(View):
    def get(self, request):
        context = initial(request)
        dept_number = context.get('dept_number')
        myChildren = [UserKB.objects.get(id=x) for x in dept_number.get_all_children().values_list('boss', flat=True)]
        if not myChildren:
            try:
                myChildren = UserKB.objects.filter(department=dept_number).exclude(id=request.user.id)
            except:
                pass
        tickets = Ticket.objects.filter(responsible__in=myChildren).exclude(status='closed')

        theme_filter = request.GET.get('theme', '')
        user_filter = request.GET.get('user', '')
        if theme_filter:
            tickets = tickets.filter(theme__iexact=theme_filter)
        if user_filter:
            user = UserKB.objects.get(id=user_filter)
            tickets = tickets.filter(responsible=user)

        text_result = found_ticket_text(len(tickets))
        themes = set(tickets.values_list('theme', flat=True))
        context['tickets'] = tickets
        context['themes'] = themes
        context['text_result'] = text_result
        context = paginate_tickets(request, tickets, context)
        return render(request, 'tickets/index.html', context=context)


class NewTickets(View):
    def get(self, request):
        context = initial(request)
        username = context.get('user_name')
        tickets = context.get('tickets')

        if username.is_authenticated:
            news = News.objects.filter(responsibleID=username.id).values_list('ticketNumber', flat=True)
            tickets = Ticket.objects.filter(id__in=news)
            context['tickets'] = tickets
            context['text_result'] = found_ticket_text(len(tickets))
            context['updates'] = len(news)

        context = paginate_tickets(request, tickets, context)
        return render(request, 'tickets/index.html', context=context)


class TicketDetail(View):
    def get(self, request, number):
        context = initial(request)
        ticket = Ticket.objects.get(number__iexact=number)
        news = News.objects.filter(Q(responsibleID = request.session.get('_auth_user_id')) &
                                   Q(ticketNumber = ticket.id))
        # удаляем "новости"
        ticketIsNew = len(news) > 0
        news.delete()

        context['ticket']=ticket
        context['ticketIsNew']= ticketIsNew
        return render(request, 'tickets/ticket_detail.html', context = context)

    def post(self, request):
        return render(request, 'tickets/index.html', context={})


class CreateTicket(LoginRequiredMixin, View):
    template = 'tickets/ticket_create_form.html'
    instance = None
    login_url = 'login_url'

    def get(self, request, number=None):
        if number:
            self.instance = Ticket.objects.get(number=number)
        user = request.user
        form = CreateTicketForm (user, instance=self.instance)

        return render( request, self.template, context={'form': form,
                                                        'user_name': user,
                                                        'dept_number': request.user.department,
                                                        })

    def post(self, request):
        user = request.user
        form = CreateTicketForm(user, request.POST or None)
        print(form.data)

        if form.is_valid():
            # for id in form.data.getlist('responsible'):
            # responsible = UserKB.objects.get(id=id)
            new_ticket = form.save(commit=False)
            # new_ticket.responsible = responsible
            new_ticket.consumer = user
            new_ticket.osn = 'Поручение от {}'.format(user)

            while not new_ticket.id:
                try:
                    nmbr = next(newNumber)
                    new_ticket.number = nmbr
                    # new_ticket.save()
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
        print('not valid form')

        return render(request, self.template, context={'form': form,
                                                        'user_name': user,
                                                        'dept_number': request.user.department,
                                                        'ticket': instance
                                                        })


class DeleteTicket(View):
    def get(self, request, number):
        context = initial(request)
        ticket = Ticket.objects.get(number__iexact=number)

        context['ticket'] = ticket
        return render(request, 'tickets/delete_ticket.html', context = context)

    def post(self, request, number):
        ticket = Ticket.objects.get(number__iexact=number)
        ticket.delete()
        return redirect(reverse('all'))


class RejectTicket(View):
    def get(self, request, number):
        context = initial(request)
        ticket = Ticket.objects.get(number__iexact=number)
        context['ticket'] = ticket
        return render(request, 'tickets/reject_ticket.html', context = context)

    def post(self, request, number):
        ticket = Ticket.objects.get(number__iexact=number)
        ticket.isSignedByResponsible = False
        ticket.save()
        return redirect(ticket)


class RedirectTicket(View):
    def get(self, request, number):
        context = initial(request)
        ticket = Ticket.objects.get(number__iexact=number)
        user = request.user
        context['ticket'] = ticket
        context['form'] = RedirectTicketForm(user=user)
        return render(request, 'tickets/redirect_ticket.html', context = context)

    def post(self, request, number):
        ticket = Ticket.objects.get(number__iexact=number)
        user = request.user
        form = RedirectTicketForm(user, request.POST or None)
        print('get from from:')

        for id in form.data.getlist('responsible'):
            signer = UserKB.objects.get(id=id)
            s = Signer()
            s.save(user=signer, ticket=ticket)

        return redirect(ticket)


class ArchivedTickets(View):
    def get(self, request):
        context = initial(request)
        username = context.get('user_name')
        archive_tickets =  Ticket.objects.filter( Q(consumer=username) | Q(responsible=username))
        archive_tickets = archive_tickets.filter(Q(status='closed') )

        theme_filter = request.GET.get('theme', '')
        user_filter = request.GET.get('user', '')

        if theme_filter:
            archive_tickets = archive_tickets.filter(theme__iexact=theme_filter)
        if user_filter:
            user = UserKB.objects.get(id=user_filter)
            archive_tickets = archive_tickets.filter(responsible=user)

        text_result = found_ticket_text(len(archive_tickets))
        context['tickets'] = archive_tickets
        context['text_result'] = text_result
        context = paginate_tickets(request, archive_tickets, context)
        return render(request, 'tickets/archive.html', context=context)

    def post(self, request):
        pass


class PlannedTickets(View):
    def get(self, request, days):
        context = initial(request)
        username = context.get('username')
        td = date.today()
        planned_ticket = Ticket.objects.filter(Q(term__range=(td, td + timedelta(int(days))))
                                               & (Q(responsible=username) | Q(consumer=username)))

        theme_filter = request.GET.get('theme', '')
        user_filter = request.GET.get('user', '')

        if theme_filter:
            planned_ticket = planned_ticket.filter(theme__iexact=theme_filter)
        if user_filter:
            user = UserKB.objects.get(id=user_filter)
            planned_ticket = planned_ticket.filter(responsible=user)

        text_result = found_ticket_text(len(planned_ticket))

        paginator = Paginator(planned_ticket, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        prev_url = '?page={}&plan={}'.format( page.previous_page_number(), days) if page.has_previous() else ''
        next_url = '?page={}&plan={}'.format( page.next_page_number(), days,) if page.has_next() else ''

        context['tickets'] = planned_ticket
        context['days'] = days
        context['text_result'] = text_result
        context['page_object'] = page
        context['is_paginated'] = is_paginated
        context['prev_url'] = prev_url
        context['next_url'] = next_url
        return render(request, 'tickets/plan.html', context=context)


class ReportedTickets (View):
    def get(self, request):
        context = initial(request)
        username = context.get('username') or None
        days = request.GET.get('report', '') or None
        td = date.today()
        reported_tickets = Ticket.objects.filter(Q(term__range=(td - timedelta(int(days)), td )) & Q(status='closed') & Q(consumer=username)) # to be changed later
        theme_filter = request.GET.get('theme', '')
        user_filter = request.GET.get('user', '')
        if theme_filter:
            reported_tickets = reported_tickets.filter(theme__iexact=theme_filter)
        if user_filter:
            user = UserKB.objects.get(id=user_filter)
            reported_tickets = reported_tickets.filter(responsible=user)
        text_result = found_ticket_text(len(reported_tickets))
        context['tickets'] = reported_tickets
        context['days'] = days
        context['text_result'] = text_result
        context = paginate_tickets(request, reported_tickets, context)
        return render(request, 'tickets/report.html', context=context)

    def post(self, request):
        context = initial(request)
        return render(request, 'tickets/report.html', context=context)