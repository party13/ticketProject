# Create your views here.

from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Signer
# from datetime import date, timedelta
from tickets.models import Ticket
from KB_Users.models import UserKB


def signer_sign(request):
    username = request.user or None
    ticket_number = request.POST.get('tn', '') or None
    # user_id = request.POST.get('un', '') or None
    if ticket_number:
        print(username)
        ticket = Ticket.objects.get(id=ticket_number)
        print (ticket)

        s = Signer.objects.filter(Q(user=username) & Q(ticket=ticket)).first()
        print(s)
        s.signing(user=username, ticket=ticket)

        return redirect(ticket)




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