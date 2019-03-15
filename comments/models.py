from django.db import models
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

    def save(self,  *args, **kwargs):
        self.when = datetime.today()
        super(Comment, self).save(*args, **kwargs)

#
# class Report(models.Model):
#     ticket = models.ForeignKey('tickets.Ticket',
#                                  on_delete='CASCADE',
#                                  related_name='to_ticket',
#                                  verbose_name='к карточке')
#
#     user = models.ForeignKey('KB_Users.UserKB',
#                              on_delete='CASCADE',
#                              related_name='from_user',
#                              verbose_name='от пользователя')
#
#     file = models.FileField(upload_to='reports/%Y/%m/%d', null=True)
#
#     text = models.TextField(null=True)
#




