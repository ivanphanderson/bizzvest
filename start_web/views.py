from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
import json
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from models_app.models import UserAccount
from .forms import RegisterUserForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.
class UsernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "Username telah terpakai, silahkan gunakan username lain!"}, status=409)
        return JsonResponse({"username_valid": True})

class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        try:
            validate_email(email)
        except ValidationError as e:
            return JsonResponse({"email_error": "Masukkan email yang benar!"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "Email telah terpakai, silahkan gunakan email lain!"}, status=409)
        return JsonResponse({"email_valid": True})


def sign_up(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user_object = form.save()
            useraccount_obj = UserAccount(user_model=user_object)
            useraccount_obj.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return HttpResponseRedirect("/")
        print(form.errors)
    else:
        form = RegisterUserForm()


    return render(request, "signup.html", {"form":form})

@csrf_exempt  # TODO
def log_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.success(request, ("Username atau Password salah, silahkan coba lagi"))
            return redirect("login")

    else:
        return render(request, "login.html", {})

def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")
