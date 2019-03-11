from django.db import models
from django.shortcuts import reverse
from datetime import date, timedelta
from django.db.models.query import QuerySet
#from .KB_users.models import KBUser
from comments.models import Comment
from history.models import TicketTermRequest


class Department(models.Model):
    departmentName = models.CharField('Наименование подразделения', max_length=25, unique=True)
    boss = models.ForeignKey('KB_Users.UserKB', on_delete='SET_NULL', null=True, related_name='Руководитель',
                           help_text='Руководитель подразделения')
    path = models.CharField(max_length=24, unique=True, editable=False,
                            help_text='Параметр, определяющий иерархию подразделения в структуре КБЮ',)
    """
    path is a field to keep hierarchy of departments, and represent which department consists of other smaller departments,
    path has strictly 2-digits format separated with dots(.) as it shown here: 01.04.03.02 or 02.01
    it means that every department could have no more than 99 'children'
    for example, department 05.03 could have such children 05.03.01, 05.03.02 ... 05.03.99
    """

    class Meta:
        ordering = ['departmentName', 'path']
        verbose_name = 'Подразделение'
        verbose_name_plural  = 'Подразделения'

    def __str__(self):
        return self.departmentName

    def save(self, *args, **kwargs):
        super(Department, self).save(*args, **kwargs)

    def get_department(self, path):
        # returns department on it's path
        return Department.objects.get(path__exact=path)

    def get_parent(self):
        # returns parent department
        parent_path = '.'.join(self.path.split('.')[:-1])
        try:
            return Department.objects.get(path__exact = parent_path)
        except:
            return 'Root'
    get_parent.short_description = "Parent department"

    def get_latest_child_number(self):
        last_child = self.get_children().last()
        if last_child:
            return int(last_child.path.split('.')[-1])
        else:
            return 1

    def get_children(self):
        # only direct children
        pattern=self.path+'.\d{2}$'
        children = Department.objects.filter(path__regex = pattern).order_by('path')
        return children.exclude(path__exact = self.path)

    # def children_list(self):
    #     return self.get_children()

    def get_all_children(self):
        # returns all children, including all children's children
        children = Department.objects.filter(path__startswith = self.path).order_by('path')
        return children.exclude(path__exact = self.path)

    def save_to(self, parent):
        assert type(parent) == Department , "Error. Invalid type received in tickets.models.save_to : {} ".format(type(parent))
        print("Saving {} to {}".format(self, parent))
        target_path = parent.path
        current_number = str(parent.get_latest_child_number() + 1)
        if len(current_number) != 2:
            current_number= '0' + current_number
        self.path = target_path + '.' + current_number
        self.save()
        return self


    def move_to(self, anotherDepartment):
        # перемещает данное подразделение и все входящие в него в подчинение другому подразделению
        # с сохранением структуры
        assert type(anotherDepartment) == Department
        target_path = anotherDepartment.path
        current_number = str(anotherDepartment.get_latest_child_number() + 1)
        if len(current_number) != 2:
            current_number= '0' + current_number
        newpath = target_path + '.' + current_number

        for child in self.get_all_children():
            #if child:
            print(child.departmentName)
            new_child_path = child.path.replace(self.path , newpath)
            print(new_child_path)
            child.path = new_child_path
            child.save()
            print('saved! ')

        self.path = newpath
        self.save()
        print('all done!')


class News(models.Model):
    responsibleID = models.CharField(max_length=10, db_index=True)
    # ticketNumber - is a ticketID releation
    ticketNumber = models.IntegerField()


class Ticket(models.Model):
    number = models.IntegerField('Номер', unique=True)
    theme = models.CharField('Тема', max_length=150, db_index=True)
    job = models.TextField('Вид работ', db_index=True)
    term = models.DateField('Срок')
    status = models.CharField(max_length=10,
                              choices=(
                                  ('active', 'действующая'),
                                  ('closed', 'закрыта'),
                                  ('prolong', 'продлена'),
                                  ('copy', 'копия')
                              )
                              )
    osn = models.CharField('Основание', max_length=150, )
    zakaz = models.CharField('Заказ', max_length=50, )
    reports = models.TextField('Отчетные материалы', max_length=200, blank=True)
    controlGK = models.BooleanField('Контроль генерального', default=False)
    isSignedByResponsible = models.BooleanField('Подписана ответственным', default=False)
    isSignedByCustomer = models.BooleanField('Подписана потребителем',default=False)
    responsible = models.ForeignKey('KB_Users.UserKB',
                                    default=1,
                                    on_delete='SET_DEFAULT',
                                    related_name='responsible',
                                    verbose_name='Ответственный')
    consumer = models.ForeignKey('KB_Users.UserKB',
                                 default=1,
                                 on_delete='SET_DEFAULT',
                                 related_name='consumer',
                                 verbose_name='Потребитель')
    class Meta:
        ordering=['term']
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'

    def __str__(self):
        return self.get_ticket_title(words=8)

    def save(self, *args, **kwargs):
        super(Ticket, self).save(*args, **kwargs)
        new = News()
        new.responsibleID = self.responsible.id
        new.ticketNumber = self.id
        new.save()
        print('Ok, news-', new.id, 'ticket.id- ', new.ticketNumber, ' responsible ID- ', new.responsibleID)

    def delete(self, *args, **kwargs):
        if News.objects.filter(ticketNumber=self.id).exists():
            new = News.objects.get(ticketNumber=self.id)
            new.delete()
        if Comment.objects.filter(ticket=self).exists():
            cmnts = Comment.objects.filter(ticket=self)
            cmnts.delete()
        if TicketTermRequest.objects.filter(ticketID=self).exists():
            ttrs = TicketTermRequest.objects.filter(ticketID=self)
            ttrs.delete()
        super(Ticket, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ticket_detail_url', kwargs={'number': self.number})

    def get_ticket_term(self):
        # 2018-12-04
        term = str(self.term).split('-')
        # 04.12.2018
        return '.'.join((term[2], term[1], term[0]))

    def get_ticket_expiration(self):
        delta = (self.term - date.today()).days
        if delta > 0 :
            exp = 'осталось {} дней'.format(str(delta))
        elif delta==0:
            exp = 'срок сегодня'
        else:
            exp = 'просрочена на {} дней'.format(str(-delta))
        return exp

    def get_ticket_title(self, words=10):
        title = str(self.job).split()[:words]
        return ' '.join(title)
    get_ticket_title.short_description = 'Заголовок'

    def get_other_job(self, words=10):
        other_job = str(self.job).split()[words:]
        return ' '.join(other_job)

    def ticket_is_out_of_term(self):
        return (self.term - date.today()).days < 0

    def get_ticket_responsible(self):
        return self.responsible

    def get_ticket_consumer(self):
        return self.consumer

    def get_resp_phone(self):
        resp_user = self.responsible
        return str(resp_user.phone)

    def get_consum_phone(self):
        consum_user = self.consumer
        return consum_user.phone

    def mayBeClosed(self):
        print('may be closed?')
        if not self.isSignedByResponsible:
            print('not signed by resp')
            return False
        if not self.isSignedByCustomer:
            print('not signed by custom')
            return False
        if not self.reports:
            print('no reports')
            return False
        if self.term < date.today():
            print('too late to close automatically')
            return False
        print('yes!')
        return True

    def mayBeClosedAutomatically(self):
        if not self.isSignedByResponsible:
            return False
        if not self.reports:
            return False
        if self.term < date.today():
            return False
        return True

    def comments(self):
        return Comment.objects.filter(ticket=self)

    def comments_quantity(self):
        return Comment.objects.filter(ticket=self).count()

    def term_requested(self):
        return TicketTermRequest.objects.filter(ticketID=self).exists()

    def term_request(self):
        try:
            return TicketTermRequest.objects.filter(ticketID=self)
        except:
            return None


    def closeTicket(self):
        self.status = 'closed'
        self.term = date.today()        #may be changed later///??
        self.save()

