from django.shortcuts import render
from .models import Comment
from tickets.models import Ticket
# Create your views here.

def add_comment(request):
    ticket_number = request.POST.get('tn', '') or None
    ticket = Ticket.objects.get(number = ticket_number)
    user = request.user
    if ticket_number:
        cmnt = Comment(user=user, ticket=ticket)
    return cmnt

