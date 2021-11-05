from django.shortcuts import render
from .forms import MessageForm
from .models import Message
from django.core import serializers
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def add_message(request):
    if request.is_ajax and request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            message = request.POST['message']
            msg = Message(email=email, message=message)
            msg.save();
            return JsonResponse({'status':'Save'})
        else:
            return JsonResponse({'status':0})
