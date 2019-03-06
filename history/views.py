from django.shortcuts import render, redirect
from .models import TicketTermRequest
from tickets.models import Ticket
from django.views.generic import View

# Create your views here.

class TermRequest(View):
    def get(self, request, number):
        ticket = Ticket.objects.get(number=number)
        context={'supervisor':''
                 ''}
        return render(request, 'history/term_request.html', context=context)

    def post(self, request, number):
        ticket = Ticket.objects.get(number=number)
        return redirect(ticket)


class TermConfirm(View):
    def get(self, request, number):
        ticket = Ticket.objects.get(number=number)
        context={'requester':'',
                 'term_change_date':'',
                 }
        return render(request, 'history/prolongate_confirm.html', context=context)

    def post(self, request, number):
        ticket = Ticket.objects.get(number=number)
        return redirect(ticket)

