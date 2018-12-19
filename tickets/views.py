from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import User, Ticket
import os
# Create your views here.


def index_page(request):
    context = {
        'updates' : str(1),
        'user_name' : os.getlogin(),
        'dept_number': str(163),
    }
    return render(request, 'tickets/index.html', context = context)


def tickets_list(request):
    tickets = Ticket.objects.all()
    context = {'tickets': tickets,
               'updates': str(77)
               }
               # 'user_name': 'юзер_пока_что'

    return render(request, 'tickets/index.html', context=context)


class TicketDetail(View):

    def get(self, request, number):
        #ticket = get_object_or_404(Ticket, number__iexact=number)
        ticket = Ticket.objects.get(number__iexact=number)
        context= {'ticket':ticket

                  }
        return render(request, 'tickets/ticket_detail.html', context = context)