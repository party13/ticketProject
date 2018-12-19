from django.db import models
from django.shortcuts import reverse
from datetime import  date, timedelta
from django.contrib.auth.models import User as UserDjango

class User(models.Model):

    userID = models.IntegerField(primary_key=True, unique=True)

    secondname = models.CharField('Фамилия', max_length=50, db_index=True)
    username = models.CharField('Имя', max_length=50)
    fathname = models.CharField('Отчество',  max_length=50)
    department = models.CharField('Отдел', max_length=50,)
    position = models.CharField('Должность', max_length=150,)
    phone = models.CharField('Телефон',max_length=20,)
    # bossID = models.ForeignKey('userID')

    #tickets = models.ManyToManyField('Ticket', blank=True, related_name='tickets')

    def __str__(self):
        return self.secondname + ' ' + str(self.username)[0] + '.' + str(self.fathname)[0] + '.'


class Ticket(models.Model):

    number = models.IntegerField(primary_key=True, unique=True, db_index=True)
    theme = models.CharField('Тема', max_length=150, db_index=True)
    job = models.TextField('Вид работ', db_index=True)
    term = models.DateField('Срок')
    status = models.CharField(max_length=10,
                              choices=(
                                  ('active','действующая'),
                                  ('closed', 'закрыта'),
                                  ('prolong', 'продлена'),
                                  ('copy','копия')
                              )
                              )
    osn = models.CharField('Основание', max_length=150,)
    zakaz = models.CharField('Заказ', max_length=50,)
    reports = models.TextField('Отчетные материалы', max_length=200, blank= True)

    controlGK = models.BooleanField('Контроль генерального', default=False)
    isRead = models.BooleanField(default=False)

    #ответственый
    responsible = models.ManyToManyField( User, related_name='Ответственый')
    # потребитель
    customer = models.ManyToManyField( User, related_name='Потребитель')

    def get_ticket_url(self):
        return reverse('ticket_detail_url', kwargs = {'number':self.number})

    def get_ticket_term(self):
        #2018-12-04
        term = str(self.term).split('-')
        #04.12.2018
        return '.'.join((term[2],term[1],term[0]))

    def get_ticket_expiration(self):
        delta = (self.term - date.today() ).days
        return  'осталось {} дней'.format(str(delta)) if delta > 0 else 'просрочена на {} дней'.format(str(-delta))

    def get_ticket_title(self, words=15):
        title = str(self.job).split()[:words]
        return ' '.join(title) + '...'

    def get_other_job(self, words=15):
        other_job = str(self.job).split()[words:]
        return ' '.join(other_job)

    def ticket_is_out_of_term(self):
        return (self.term - date.today() ).days < 0

    def get_ticket_responsible(self):
        return self.responsible.last()

    def get_ticket_customer(self):
        return self.customer.first()

    def get_resp_phone(self):
        resp_user = self.responsible.last()
        return str(resp_user.phone)

    def get_custom_phone(self):
        custom_user = self.customer.last()
        return custom_user.phone

    def __str__(self):
        return self.get_ticket_title(words=8)