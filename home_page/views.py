from django.shortcuts import render
from .forms import MessageForm
from .models import Message
from django.core import serializers
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def add_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            message = request.POST['message']
            msg = Message(email=email, message=message)
            msg.save();
            return JsonResponse({'status':'Save'})
        else:
            return JsonResponse({'status':0})

def json_message(request):
    messages = Message.objects.all()
    data = serializers.serialize('json', messages)
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def save_api(request):
    data = json.loads(request.body)
    email = data["email"]
    message = data["message"]
    print(f"Email: {email}\nPesan: {message}")
    msg = Message(email=email, message=message)
    msg.save()
    return JsonResponse({"status": "Saved", "email": email, "message": message})
