from django.shortcuts import render, redirect
from .models import TicketTermRequest
from tickets.models import Ticket, News
from django.views.generic import View
from .forms import TermRequestForm
from tickets.forms import TermConfirmForm
from datetime import date

# Create your views here.

class TermRequest(View):
    def get(self, request, number):
        form = TermRequestForm()
        # form.fields['text'].attrs={'cols':10, 'rows': 3}
        txt = form.fields['text']
        txt.attrs = {'cols':10, 'rows': 3}
        print (txt)
        ticket = Ticket.objects.get(number=number)
        supervisor = ticket.consumer
        context={'supervisor':supervisor,
                 'ticket':ticket,
                 'lastdate':ticket.term,
                 'form':form}
        return render(request, 'history/term_request.html', context=context)

    def post(self, request, number):
        ticket = Ticket.objects.get(number=number)
        user = request.user or None
        dept_number = user.department or None
        form = TermRequestForm(request.POST)
        if form.is_valid():
            term_request = form.save(commit=False)
            term_request.ticketID = ticket
            term_request.toWhom = ticket.consumer
            term_request.user = request.user
            # term_request.when = date.today()
            term_request.save()
            news = News(responsibleID=term_request.toWhom.id, ticketNumber=ticket.id)
            news.save()
            return redirect(ticket)
        print('not valid')
        return render(request, 'history/term_request.html', context={'form':form,
                                                                     'user_name': user,
                                                                     'dept_number': dept_number,
                                                                     'ticket': ticket
        })


def termConfirm(request, number):
    ticket = Ticket.objects.get(number=number)
    user = request.user or None
    dept_number = user.department or None

    termRequest = TicketTermRequest.objects.filter(ticketID=ticket).last()
    explain = termRequest.text
    requester = termRequest.user
    term_change_date = termRequest.newDate
    context = {'ticket': ticket,
               'requester': requester,
               'term_change_date': term_change_date,
               'term_change_explain': explain,
               'user_name': user,
               'dept_number': dept_number,
               }
    form = TermConfirmForm(newterm=term_change_date)
    if request.method=="GET":

        context['form'] = form
        return render(request, 'history/term_confirm.html', context=context)

    form = TermConfirmForm( term_change_date, request.POST or None )
    if form.is_valid():
        term = form.cleaned_data['term']
        print (term)
        ticket.term = term
        ticket.save()
        termRequest.delete()

        return redirect(ticket)
    else:

        context['form'] = form
        return render(request, 'history/term_confirm.html', context=context)




