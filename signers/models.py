from django.db import models
from datetime import datetime

# from tickets.models import News

# Create your models here.


class Signer(models.Model):
    '''
    addititonal model for signing tickets by users,
    who are not responsible or consumer of a ticket,
    but their sign is essential for ticket life-cycle.
    For ex. consumer-boss can redirect the ticket for his(or her) workers.
    '''
    ticket = models.ForeignKey('tickets.Ticket',
                                 on_delete='CASCADE',
                                 related_name='ticket_to_sign',
                                 verbose_name='карточка')

    user = models.ForeignKey('KB_Users.UserKB',
                               on_delete='CASCADE',
                               related_name='signing_user',
                               verbose_name='визирующий')
    isSigned = models.BooleanField(default=False)
    signDate = models.DateField(null=True)


    def __str__(self):
        return 'User{}  ---- signed:{}'.format(self.user, self.isSigned)


    def save(self, ticket, user, makeNews=True, *args, **kwargs):
        self.ticket = ticket
        self.user = user
        super(Signer, self).save(*args, **kwargs)
        if makeNews:
            from tickets.models import News
            n = News(responsibleID = user.id, ticketNumber=ticket.id)
            n.save()



    def signing(self, ticket, user):
        self.isSigned = True
        self.signDate = datetime.today()
        self.save(ticket=ticket, user=user, makeNews=False)

    def remove_sign(self, ticket, user):
        self.isSigned = False
        self.signDate = None
        self.save(ticket=ticket, user=user, makeNews=False)



