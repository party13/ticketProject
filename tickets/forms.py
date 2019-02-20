from django.forms import ModelForm, ModelMultipleChoiceField
from django.forms import SelectDateWidget, CheckboxSelectMultiple
from KB_Users.models import UserKB
# from django import forms
from .models import Ticket



class CreateTicketForm(ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        print('initing form')
        super(CreateTicketForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['responsible'].queryset = user.get_children() or user.get_my_workers()

    class Meta:
        model = Ticket
        fields = ['theme', 'job', 'term', 'responsible']
        labels = {
            'responsible': 'Ответственный',
        }
        # field_classes = {'responsible' :  ModelMultipleChoiceField}

        widgets = {
            # 'term': SelectDateWidget,
            # 'responsible' : CheckboxSelectMultiple
                   }

