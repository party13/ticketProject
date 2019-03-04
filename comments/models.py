from django.db import models
# from tickets.models import Ticket
from datetime import datetime

class Comment(models.Model):
    ticket = models.ForeignKey('tickets.Ticket',
                                 on_delete='CASCADE',
                                 related_name='ticket',
                                 verbose_name='карточка')

    user = models.ForeignKey('KB_Users.UserKB',
                               on_delete='CASCADE',
                               related_name='user',
                               verbose_name='пользователь')
    text = models.TextField()

    when = models.DateTimeField(editable=False)

    def __str__(self):
        return ' {} - {}'.format(self.text, self.when)

    def save(self, ticket = None, user=None, *args, **kwargs):
        if ticket and user:
            self.when = datetime.today()
            super(Comment, self).save(*args, **kwargs)
            print('ok, cmnt')



