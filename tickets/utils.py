from datetime import date
from .models import News


def user_dept(request):
    """ gets user_name, department, and news from request """
    if request.user.is_authenticated:
        username = request.user
        updates = News.objects.filter(responsibleID__exact=username.id).count()
        dept_number = username.department
    else:
        updates = 0
        username = None
        dept_number = ''
    return username, dept_number, updates


def generate_number():
    # generates ticketNumber when created by user
    td = ''.join((str(date.today())).split('-'))
    # num = str(n)
    for i in range(1000):
        # ожидается, что не более 1000 карточек в день будет создаваться
        # самими пользователями по всему предприятию
        yield td+str(i)


def found_ticket_text(quantity):
    quantity = str(quantity)
    if quantity==0:
        return ''
    if quantity[-1] in '567890' or quantity in ['11', '12', '13', '14']:
        return ' {} карточек'.format(quantity)
    elif quantity[-1] in '234':
        return ' {} карточки'.format(quantity)
    else:
        return ' {} карточка'.format(quantity)

