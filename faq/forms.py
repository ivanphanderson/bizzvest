from django.forms import ModelForm, Textarea, TextInput
from .models import Faq

class NoteForm(ModelForm):
    class Meta:
        model = Faq
        fields = ['nama', 'pertanyaan']