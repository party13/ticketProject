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
