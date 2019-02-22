from django.forms import ModelForm, Form
#     ModelMultipleChoiceField
# from django.forms import SelectDateWidget, CheckboxSelectMultiple
from django.contrib.admin.widgets import AdminDateWidget
from .models import Ticket
from datetime import date
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives


class CreateTicketForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        # print('initing form')
        super(CreateTicketForm, self).__init__(*args, **kwargs)
        self.fields['term'].widget = AdminDateWidget()
        if user:
            self.fields['responsible'].queryset = user.get_children() or user.get_my_workers()

    def clean_term(self):
        # automatically raised method when cleaning field 'term'
        # during form validation . return data is MUST
        data = self.cleaned_data['term']
        if data < date.today():
            raise ValidationError('Назначение срока "на вчера" Вам не к лицу. Поставьте корректную дату', code='invalid')
        return data


    class Meta:
        model = Ticket
        fields = ['theme', 'job', 'term', 'responsible']
        labels = {
            'responsible': 'Ответственный',
        }

        autocomplete_fields = ['theme']

        widgets = {
            # 'term': AdminDateWidget,
            # 'responsible' : CheckboxSelectMultiple
                   }

class ShareTicketForm(Form):

    def save(self, user, link):
        email = self.cleaned_data["email"]
        subject = 'Карточка'
        from_email = user.email
        body = r'Карточка {}'.format(link)

        email_message = EmailMultiAlternatives(subject, body, from_email, [email])
        email_message.send()