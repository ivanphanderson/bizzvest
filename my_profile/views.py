from django.shortcuts import render
from models_app.models.UserAccount import UserAccount
from models_app.models.InvestorAccount import InvestorAccount
from models_app.models.EntrepreneurAccount import EntrepreneurAccount
from my_profile.forms import PhotoForm, ProfileForm, FormSpesial
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages


import json
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
    is_valid, ret_obj = validate_toko_id_by_GET_req(req)
    if not is_valid:
        return ret_obj

    company:Company = ret_obj[0]
    logged_in_acc = get_logged_in_user_account(req)
    is_company_owner_account = logged_in_acc is not None and (
            logged_in_acc.user_model.username == company.pemilik_usaha.account.user_model.username
    )

    informasi_saham = InformasiSaham(company)

    ret = {
        'is_curr_client_the_owner': 1 if is_company_owner_account else 0,
        'nama_merek': company.nama_merek,
        'nama_perusahaan': company.nama_perusahaan,
        'images': [i.img.url for i in company.companyphoto_set.all().order_by("img_index")] or [
            static("img/no pict.png")
        ],
        'status_verifikasi': company.status_verifikasi,
        'tanggal_berakhir': defaultfilters.date(company.end_date, "d M Y"),
        'kode_saham': company.kode_saham,
        'sisa_waktu': ubah_jadi_bulan_atau_tahun_jika_perlu(
            number_of_days_from_today(company.end_date)
        ),
        'periode_dividen': company.dividen,
        'alamat': company.alamat,
        'deskripsi': company.deskripsi,
        'alamat_proposal': company.proposal.url if company.proposal else "",
        'owner': {
            'full_name': company.pemilik_usaha.account.full_name,
            'username': company.pemilik_usaha.account.user_model.username,
            'photo_profile': company.pemilik_usaha.account.photo_profile.url,
        },
        'nilai_lembar_saham': company.nilai_lembar_saham,
        'jumlah_lembar_saham': company.jumlah_lembar,
        'jumlah_lembar_saham_tersisa': informasi_saham.lembar_saham_tersisa,
    }
    return HttpResponse(json.dumps(ret, indent=4, sort_keys=True, default=str))
