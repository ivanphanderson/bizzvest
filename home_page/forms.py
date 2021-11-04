from home_page.models import Message
from django.forms import ModelForm


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
