from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from .forms import RegisterUserForm

# Create your views here.
def sign_up(request):
    if request.method == "POST":
	    form = RegisterUserForm(request.POST)
	    if form.is_valid():
		    form.save()
		    username = form.cleaned_data['username']
		    password = form.cleaned_data['password1']
		    user = authenticate(username=username, password=password)
		    login(request, user)
		    messages.success(request, ("Registration Successful!"))
		    return HttpResponseRedirect('')
    else:
    	form = RegisterUserForm()


    return render(request, "signup.html", {'form':form})

def log_in(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('login')

	else:
		return render(request, "login.html", {})

def log_out(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('home')
