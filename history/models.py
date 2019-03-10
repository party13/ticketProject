from django.db import models
from datetime import date, timedelta

class TicketTermRequest(models.Model):
    ticketID = models.ForeignKey('tickets.Ticket',
                                 on_delete='CASCADE',
                                 related_name='ticket_history')
    user = models.ForeignKey('KB_Users.UserKB',
                             on_delete='CASCADE',
                             related_name='origin')
    toWhom = models.ForeignKey('KB_Users.UserKB',
                               on_delete='CASCADE',
                               related_name='destination', null=True)
    when = models.DateTimeField()
    text = models.TextField()
    newDate = models.DateField(default=None)

    def save(self, *args, **kwargs):
        self.when = date.today()
        super(TicketTermRequest, self).save(*args, **kwargs)
        print('ok, new term request')


# class Routing(models.Model):
#     """model for tracking changes in tickets"""
#
#     operation = models.CharField(max_length=10,
#                               choices=(
#                                   ('create', 'создана'),
#                                   ('redirect', 'адресована'),
#                                   ('prolongate', 'продлена'),
#                                   ('copy', 'скопирована'),
#                                   ('attach', 'приложены материалы'),
#                                   ('sign', 'подписана'),
#                                   ('close', 'закрыта'),
#                               )
#                               )
#
#
#     def create_ticket(self, ticketID, who):
#         pass
#
#     def redirect_ticket(self):
#         pass
#
#     def change_ticket_term(self):
#         pass
#
#     def copy_ticket(self):
#         pass
#
#     def attach_ticket_reports(self):
#         pass
#
#     def sign_ticket(self):
#         pass
#
#     def close_ticket(self):
#         pass


