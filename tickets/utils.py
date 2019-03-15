from datetime import date
from .models import News, Ticket
from KB_Users.models import UserKB
from signers.models import Signer
from django.db.models import Q
from django.core.paginator import Paginator



def initial(request, context=None):
    """ gets user_name, department, and news from request """
    if not context:
        context = {}
    if request.user.is_authenticated:
        username = request.user
        updates = News.objects.filter(responsibleID=username.id).count()

        tickets = Ticket.objects.filter(Q(responsible = username) |
                                        Q(id__in=Signer.objects.filter(user=username).values_list('ticket', flat=True)))
        tickets = tickets.exclude(status='closed')
        dept_number = username.department
        themes = set(tickets.values_list('theme', flat=True))
        text_result = found_ticket_text(len(tickets))
    else:
        updates = 0
        username = None
        dept_number = None
        tickets = None
        themes = None
        text_result = None

    context['text_result'] = text_result
    context['user_name'] = username
    context['dept_number'] = dept_number
    context['updates'] = updates
    context['tickets'] = tickets
    context['themes'] = themes

    return context

def generate_number():
    # generates ticketNumber when created by user
    td = ''.join((str(date.today())).split('-'))
    for i in range(1000):
        # ожидается, что не более 1000 карточек в день будет создаваться
        # самими пользователями по всему предприятию
        yield td+str(i)


def paginate_tickets(request, tickets, context):
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.page(page_number)
    is_paginated = page.has_other_pages()
    prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
    next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''
    context['page_object'] = page
    context['is_paginated'] = is_paginated
    context['prev_url'] = prev_url
    context['next_url'] = next_url
    return context


def found_ticket_text(quantity):
    quantity = str(quantity)
    if quantity==0:
        return ''
    if quantity[-1] in '567890' or quantity in ['11', '12', '13', '14']:
        return ' {} карточек'.format(quantity)
    elif quantity[-1] in '234':
        return ' {} карточки'.format(quantity)
    else:
        return ' {} карточка'.format(quantity)


def ticket_signer_as_users(ticket):
    return UserKB.objects.filter(id__in = Signer.objects.filter(ticket=ticket).values_list('user', flat=True))

def ticket_signers(ticket):
    return Signer.objects.filter(ticket=ticket)



