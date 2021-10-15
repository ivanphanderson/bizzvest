from django.forms import ModelForm
from .models import Faq

class NoteForm(ModelForm):
    class Meta:
        model = Faq
        fields = '__all__'
