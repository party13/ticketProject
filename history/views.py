from django.shortcuts import render, redirect
from .models import TicketTermRequest
from tickets.models import Ticket
from django.views.generic import View
from .forms import TermRequestForm
from datetime import date

# Create your views here.

class TermRequest(View):
    def get(self, request, number):
        form = TermRequestForm()
        ticket = Ticket.objects.get(number=number)
        supervisor = ticket.consumer
        context={'supervisor':supervisor,
                 'ticket':ticket,
                 'lastdate':ticket.term,
                 'form':form}
        return render(request, 'history/term_request.html', context=context)

    def post(self, request, number):
        ticket = Ticket.objects.get(number=number)
        form = TermRequestForm(request.POST)
        if form.is_valid():
            term_request = form.save(commit=False)
            term_request.ticketID = ticket
            term_request.toWhom = ticket.consumer
            term_request.user = request.user
            # term_request.when = date.today()
            term_request.save()
            return redirect(ticket)
        print('not valid')
        return render(request, 'history/term_request.html', context={'form':form})


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

