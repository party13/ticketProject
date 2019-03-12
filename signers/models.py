from django.db import models
from datetime import datetime

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


    def signing(self):
        self.isSigned=True
        self.signDate = datetime.today()

    def remove_sign(self):
        self.isSigned = False


