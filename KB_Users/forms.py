import random
from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.forms import ModelForm
from .models import UserKB

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


class UserForm(ModelForm):
    class Meta:
        model = UserKB
        fields = ['secondName', 'firstName',  'fathName', 'department', 'phone', 'email', 'tabelNumber']


class RegisterForm(ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, help_text="пароли должны совпадать")

    class Meta:
        model = UserKB
        fields = ['userName', 'tabelNumber']
        labels = {'userName': 'Имя пользователя'}
        help_text = {'userName': 'используется для входа на сайт',
                     'tabelNumber':'используется для восстановления доступа'}

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
