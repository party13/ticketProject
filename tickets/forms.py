from django.forms import ModelForm
from .models import Ticket

class CreateTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['number', 'theme', 'job', 'term', 'responsible']