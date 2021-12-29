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

    # profil = request.user.useraccount
    # response = {'profil':profil}

    # data = json.loads(response.body)
    # str_data = serialize('json', response)
    # data = json.loads(str_data)
    # return JsonResponse(data, content_type="application/json")
    # print(response)
    # print(profil.full_name)

    # is_valid, ret_obj = validate_toko_id_by_GET_req(req)
    # if not is_valid:
    #     return ret_obj

    # company:Company = ret_obj[0]
    # logged_in_acc = get_logged_in_user_account(req)
    # is_company_owner_account = logged_in_acc is not None and (
    #         logged_in_acc.user_model.username == company.pemilik_usaha.account.user_model.username
    # )

    # informasi_saham = InformasiSaham(company)
    logged_in_acc = get_logged_in_user_account(req)
    print(logged_in_acc)
    ret = {
        # nanti klo udah ada loginnya, tambahin if if an kalo misal dia belom ada nama lengkap, return "belum ada nama lengkap"
        'csrf_token': "3278622dadsad",
        'nama_lengkap': 'Raihansyah Yoga Adhitama',
        'username': "uhuydee",
        'phone_number': "08571471",
        'status_verifikasi': "Pengusaha dan Investor",
        'jenis_kelamin': "Laki-laki",
        'deskripsi_diri': "Aku adalah anak gembala",
        'alamat': "Jalan jaha no 9487329 kelurahan panjaitan",
        'email': "radityaakmal@gmail.com",
        'photo_profile': "https://media.istockphoto.com/photos/hot-air-balloons-flying-over-the-botan-canyon-in-turkey-picture-id1297349747",

        # # dibawah ini dipake kalo loginnya udah bisa
        # 'csrf_token': csrf.get_token(req),
        # 'nama_lengkap': logged_in_acc.full_name if logged_in_acc.full_name else "",
        # 'username': logged_in_acc.user_model.username if logged_in_acc is not None else "none.",
        # 'phone_number': logged_in_acc.phone_number,
        # 'status_verifikasi': "Pengusaha dan Enterpreneur" if logged_in_acc.is_entrepreneur and logged_in_acc.is_investor else "",
        # # 'Investor' : "Investor" if logged_in_acc.is_investor else "",
        # 'jenis_kelamin': logged_in_acc.gender,
        # 'deskripsi_diri': logged_in_acc.deskripsi_diri,
        # 'alamat': logged_in_acc.alamat,
        # 'email': logged_in_acc.user_model.email,
        # 'photo_profile': logged_in_acc.photo_profile,
        }
    return HttpResponse(json.dumps(ret, indent=4, sort_keys=True, default=str))


def my_profile_API(req:WSGIRequest):
    addtitional_problems = []
    logged_in_account = get_logged_in_user_account(req)
    # if (logged_in_account is None):
    #     return HttpResponseRedirect(get_login_url())
    if (req.method == 'POST'):
        form = ProfileForm(req.POST)
        form_spesial= FormSpesial(req.POST)
        if form.is_valid() and form_spesial.is_valid():
            form.save()
            form_spesial.save()
            saved_obj:UserAccount = form.save()
            return HttpResponse(
                json.dumps({
                    'csrf_token': 432423423 ,
                    'nama_lengkap': 'sjsjsjs',
                    'username': "jdsjdjsjds",
                    'phone_number': "08571471",
                    'status_verifikasi': "Pengusaha dan Investor",
                    'jenis_kelamin': "Laki-laki",
                    'deskripsi_diri': "Aku adalah anak gembala",
                    'alamat': "Jalan jaha no 9487329 kelurahan panjaitan",
                    'email': "radityaakmal@gmail.com",
                    'photo_profile': "https://media.istockphoto.com/photos/hot-air-balloons-flying-over-the-botan-canyon-in-turkey-picture-id1297349747",
                }), content_type="application/json"
            )


