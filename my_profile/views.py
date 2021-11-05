from django.shortcuts import render
from models_app.models.UserAccount import UserAccount
from models_app.models.InvestorAccount import InvestorAccount
from models_app.models.EntrepreneurAccount import EntrepreneurAccount
from my_profile.forms import PhotoForm, ProfileForm, FormSpesial
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
class DoesProblemExist():
    def __init__(self):
        pass


class FormErrors():
    def __init__(self, errors):
        dictionary = errors.as_data()
        fields_list =  ['usermail',
                       'email'
                        ]

        self.does_problem_exist = DoesProblemExist()

        no_error = (ValidationError("") ,)
        for attr_name in fields_list:
            temp:ValidationError = dictionary.get(attr_name, no_error)[-1]
            setattr(self, attr_name, temp.message)
            setattr(self.does_problem_exist, attr_name, "problem" if (attr_name in dictionary) else "no-problem")

@login_required
def index(request):
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/start-web/login")
    profil = request.user.useraccount
    response = {'profil':profil}
    return render(request, 'tampilan_profil.html', response)



@login_required
def ganti_profil(request):
    # print("asdfgskjhdfs")
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/start-web/login")
    profil = request.user.useraccount
    context ={"profil" : profil}
    # create object of form
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profil)
    form_khusus = FormSpesial(request.POST or None, request.FILES or None, instance=profil.user_model)
    # check if form data is valid
    print("jksbdk", request.method, request.POST)
    if request.method == "POST" :
        print("asdsakhsa", form.is_valid(), form_khusus.is_valid())
        print(form.errors, form_khusus.errors)
        if form.is_valid() and form_khusus.is_valid():
            # save the form data to model
            form.save()
            form_khusus.save()
            return HttpResponseRedirect('/my-profile/')

        else:
            messages.info(request, 'Pastikan email, username, dan nama lengkap yang anda masukkan memenuhi syarat')
            messages.info(request, 'Nama lengkap maksimal 23 huruf (termasuk spasi)')
            messages.info(request, 'Pastikan email unik')
            messages.info(request, 'Pastikan username unik')
            print("email tidak unik")
        
            
        
  
    context['form']= form
    return render(request, 'form_gantiprofil.html', context)

@login_required
def ganti_foto(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/start-web/login")
    profil = request.user.useraccount
    context ={"profil" : profil}
    form = PhotoForm(request.POST or None, request.FILES or None, instance=profil)

    
    if request.method == "POST" :
        
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        
            
        
    context['form']= form
    return render(request, 'form_gantiprofil.html', context)