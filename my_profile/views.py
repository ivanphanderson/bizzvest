from json.encoder import JSONEncoder
from django.shortcuts import render
from models_app.models import Company
from models_app.models.UserAccount import UserAccount
from models_app.models.InvestorAccount import InvestorAccount
from models_app.models.EntrepreneurAccount import EntrepreneurAccount
from my_profile.forms import PhotoForm, ProfileForm, FormSpesial
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from halaman_toko.authentication_and_authorization import get_logged_in_user_account

from django.core.serializers import serialize

import json
import os
import re

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.middleware import csrf


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
            messages.info(request, 'Pastikan email unik, dan tidak boleh memasukkan email yang pernah digunakan sebelumnya')
            messages.info(request, 'Pastikan username unik')
            messages.info(request, 'Pastikan nomor handphone diawali digit "0" dan berjumlah minimal 11 digit angka ')
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

@csrf_exempt
def my_profile_json(req:WSGIRequest):
    logged_in_acc = get_logged_in_user_account(req)
    # print(logged_in_acc.photo_profile)
    ret = {
        'csrf_token': csrf.get_token(req),
        'full_name': logged_in_acc.full_name if logged_in_acc.full_name else "",
        'username': logged_in_acc.user_model.username,
        'phone_number': logged_in_acc.phone_number,
        'investor': 1 if logged_in_acc.is_investor else 0,
        'enterpreneur': 1 if logged_in_acc.is_entrepreneur else 0,
        'gender': 'Laki-laki' if logged_in_acc.gender=="laki_laki" else 'Perempuan' if logged_in_acc.gender=="perempuan" else "Pilih jenis kelamin",
        'deskripsi_diri': logged_in_acc.deskripsi_diri,
        'alamat': logged_in_acc.alamat,
        'email': logged_in_acc.user_model.email,
        'photo_profile': logged_in_acc.photo_profile,
        }
    return HttpResponse(json.dumps(ret, indent=4, sort_keys=True, default=str))

@csrf_exempt
def my_profile_API(req:WSGIRequest):
    addtitional_problems = []
    logged_in_account = get_logged_in_user_account(req)
    profil = logged_in_account
    global response
    if logged_in_account is None:
        return HttpResponseRedirect(get_login_url())
    if req.method == 'POST':
        form = ProfileForm(req.POST or None,instance=profil)
        form_spesial = FormSpesial(req.POST or None,instance=profil.user_model)
        print(form.errors.as_data())
        print(form_spesial.errors.as_data())
        success = False
        success_special = False
        if form.is_valid():
            form.save()
            success = True
            
        if form_spesial.is_valid():
            form_spesial.save()
            success_special = True
            
        return HttpResponse(
            json.dumps({
                'SUCCESS' :1 if success else 0,
                'SUCCESS SPECIAL' : 1 if success_special else 0,
            }), content_type="application/json"
        )

        
    else :
        return HttpResponse(
            json.dumps({
                "SUCCESS" : 0,
            }), content_type="application/json"
        )

@csrf_exempt
def foto_API(req:WSGIRequest) :
    logged_in_account = get_logged_in_user_account(req)
    profil = logged_in_account
    global response
    if logged_in_account is None:
        return HttpResponseRedirect(get_login_url())
    if req.method == 'POST':
        form_foto = PhotoForm(req.POST or None, req.FILES or None,instance=profil)
        print(form_foto.errors.as_data())
        success_foto = False
        if form_foto.is_valid():
            form_foto.save()
            print(profil.photo_profile)
            print(profil.user_model.username)
            success_foto = True
            

        return HttpResponse(
            json.dumps({
                'SUCESS FOTO': 1 if success_foto else 0,
            }), content_type="application/json"
        )

        
    else :
        return HttpResponse(
            json.dumps({
                "SUCCESS" : 0,
            }), content_type="application/json"
        )


