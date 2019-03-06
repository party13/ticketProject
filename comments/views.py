from django.shortcuts import render, redirect
from .models import Comment
from tickets.models import Ticket
from django.views.generic import View

# Create your views here.

class TicketComment(View):
    template = 'comments/comments.html'
    def get(self, request, number):
        ticket = Ticket.objects.get(number=number)
        comments = Comment.objects.filter(ticket=ticket)
        return render(request, self.template, context={'comments':comments,
                                                       'ticket': ticket,
                                                       'user_name':request.user,
                                                       'updates':0,
                                                       'dept_number':request.user.department })

    def post(self,request):
        return render(request, self.template, context={})


def all_comments(request, tn):
    if request.method=='get':
        ticket = Ticket.objects.get(number=tn)
        comments = Comment.objects.filter(ticket=ticket)       #to change!
        return render('comments.html', context=comments)


def add_comment(request):
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




