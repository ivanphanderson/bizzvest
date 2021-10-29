from django.shortcuts import render
from models_app.models.UserAccount import UserAccount
from my_profile.forms import ProfileForm
from django.http.response import HttpResponseRedirect

# Create your views here.
def index(request):
    profil = UserAccount.objects.all().values()
    response = {'profil':profil}
    return render(request, 'tampilan_profil.html', response);

# def ganti_password(request):
#     context ={}
  
#     # create object of form
#     form = PasswordForm(request.POST or None, request.FILES or None)
      
#     # check if form data is valid
#     if form.is_valid():
#         # save the form data to model
#         form.save()
#         return HttpResponseRedirect('form_gantiprofil.html')
  
#     context['form']= form
#     return render(request, 'form_gantipassword.html', context)

def ganti_profil(request):
    context ={}
  
    # create object of form
    form = ProfileForm(request.POST or None, request.FILES or None)
      
    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()
        return HttpResponseRedirect('')
  
    context['form']= form
    return render(request, 'form_gantiprofil.html', context)