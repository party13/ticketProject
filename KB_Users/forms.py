import random
from django import forms
from django.contrib.auth.forms import PasswordResetForm
#from .models import UserKB

from django.core.mail import EmailMultiAlternatives


def create_random_pasword(length=6):
    alphabet= '2346789abcdefghkmnprstquxyzABCFEGTRPWKMNQ_'
    passw = ''
    for i in range(length):
        passw+=random.choice(alphabet)
    return passw


class ResetPasswordForm(PasswordResetForm):
    tabelNum = forms.IntegerField(label="Табельный №")

    def save(self, user):
        email = self.cleaned_data["email"]
        new_password = create_random_pasword(7)
        subject = 'Смена пароля на сайте Карточек'
        from_email = 'admin@test1.ua' #hardcoded mail
        body = r'Уважаемый {} {}! Это письмо отправлено Вам автоматически, ' \
               'так как Вы запросили сброс пароля на сайте Карточек. ' \
               'Ваш новый пароль : {} . ' \
               'Вы можете сменить его в своем профиле на сайте. ' \
               'Если Вы не предпринимали попыток сменить пароль, ' \
               'пожалуйста игнорируйте это письмо'.format(user.firstName, user.fathName, new_password)

        email_message = EmailMultiAlternatives(subject, body, from_email, [email])
        user.set_password(new_password)
        user.save()
        email_message.send()



