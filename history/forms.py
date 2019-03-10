from django.forms import ModelForm, Form
#     ModelMultipleChoiceField
from django import forms
# from django.forms import SelectDateWidget, CheckboxSelectMultiple
from django.contrib.admin.widgets import AdminDateWidget
from .models import TicketTermRequest
from datetime import date
from django.core.exceptions import ValidationError
# from django.core.mail import EmailMultiAlternatives
# from django.forms.widgets import DateInput

class TermRequestForm(ModelForm):

    def clean_newDate(self):
        # automatically raised method when cleaning field 'term'
        # during form validation . return data is MUST
        data = self.cleaned_data['newDate']
        if data < date.today():
            raise ValidationError('Нельзя использовать прошедшую дату. Поставьте корректную дату', code='invalid')
        return data

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) < 10:
            raise ValidationError('Слишком лаконичное обоснование.', code='invalid')
        return data

    class Meta:
        model = TicketTermRequest
        fields = ['text', 'newDate']
        labels = {
            'text': 'Обоснование',
            'newDate': 'Предлагаемый срок'
        }

        widgets = {
             'newDate': AdminDateWidget(),
                   }