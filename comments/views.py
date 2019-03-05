from django.shortcuts import render, redirect
from .models import Comment
from tickets.models import Ticket
# Create your views here.



def all_comments(request, tn):
    if request.method=='get':
        ticket = Ticket.objects.get(number=tn)
        comments = Comment.objects.filter(ticket=ticket)       #to change!
        return render('comments.html', context=comments)


def add_comment(request, tn):
    text = request.POST.get('comment_text', '') or None
    ticket_number = request.POST.get('tn', '') or None
    ticket = Ticket.objects.get(number = ticket_number)
    user = request.user
    if ticket_number and text:
        cmnt = Comment(user=user, ticket=ticket, text=text)
        cmnt.save()
        print (cmnt.id)
    return redirect(ticket)

def delete_comment(request, id):
    if Comment.objects.filter(id=id).exists():
        cmnt = Comment.objects.get(id=id)
        ticket = cmnt.ticket

        cmnt.delete()
        return redirect(ticket)




