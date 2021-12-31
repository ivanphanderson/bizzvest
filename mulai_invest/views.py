from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from halaman_toko.authentication_and_authorization import *

from models_app.models.UserAccount import UserAccount
from models_app.models import Company
from models_app.models import Stock
import traceback

# probably delete it later
from django.contrib.auth.models import User
# Create your views here.

def update_saldo_ajax(request):
    if request.method == "POST":
        saldoo = request.user.useraccount.saldo
        saldo1 = int(saldoo)+int(request.POST.get('saldo', None))
        if saldo1>2000000000:
            return JsonResponse({'user': {'message': 'Saldo maksimal Anda adalah 2 miliar Rupiah', 'status': 'fail'}})
        if saldo1<0:
            return JsonResponse({'user': {'message': 'Saldo minimal adalah 0', 'status': 'fail'}})

        obj = get_object_or_404(UserAccount, user_model=request.user)
        obj.saldo=saldo1
        obj.save()

        user = {'id':obj.id,'saldo':obj.saldo, 'status': 'success'}


        data = {
            'user': user
        }
        return JsonResponse(data)

def beli_saham(request):
    if request.method=="POST":
        saldoo = request.user.useraccount.saldo
        saham_dibeli = int(request.POST.get("jumlah_lembar_saham"))

        if saham_dibeli < 1:
            return JsonResponse({'user': {'message': 'Minimal pembelian 1 lembar', 'status': 'fail'}})

        company_id= int(request.POST.get("id", None))
        company_obj=Company.objects.filter(id=company_id).first()

        company_stock = Stock.objects.filter(company=company_obj)
        lembar_saham_terjual = 0
        for stock in company_stock:
            lembar_saham_terjual += stock.jumlah_lembar_saham

        sisa_lembar = int(company_obj.jumlah_lembar) - int(lembar_saham_terjual)
        sisa_lembar_after = int(sisa_lembar) - int(saham_dibeli)
        if sisa_lembar_after < 0:
            return JsonResponse({'user': {'message': 'Saham yang tersisa pada perusahaan ini hanya ' + str(sisa_lembar) + ' lembar', 'status': 'fail'}})

        lembar_saham_terjual += saham_dibeli

        saldo1 = int(saldoo) - int(saham_dibeli) * int(company_obj.nilai_lembar_saham)
        if saldo1 < 0:
            return JsonResponse({'user': {'message': 'Saldo Anda tidak cukup 😢', 'status': 'fail'}})
        
        profile_obj = get_object_or_404(UserAccount, user_model=request.user)
        profile_obj.saldo=saldo1
        profile_obj.save()

        stock_obj = None
        
        is_exist = Stock.objects.filter(holder=request.user, company=company_obj)
        if(is_exist.first()):
            
            jumlah_lembar_saham1 = (request.POST.get('jumlah_lembar_saham', None))
            stock_obj = is_exist.first()
            jumlah_lembar_saham = int(stock_obj.jumlah_lembar_saham)
            jumlah_lembar_saham+=int(jumlah_lembar_saham1)
            stock_obj.jumlah_lembar_saham=jumlah_lembar_saham
            stock_obj.save()

        else:
            jumlah_lembar_saham1 = int(request.POST.get('jumlah_lembar_saham', None))
            stock_obj = Stock.objects.create(
                holder = request.user,
                company = company_obj,
                jumlah_lembar_saham = jumlah_lembar_saham1
            )

        user = {
            'saldo':profile_obj.saldo, 
            'saham_tersisa': sisa_lembar_after, 
            'saham_tanam': stock_obj.jumlah_lembar_saham,
            'saham_terjual': lembar_saham_terjual,
            'status': 'success'
        }

        data = {'user': user}
        return JsonResponse(data)

@csrf_exempt
def get_invest_stuff(request):
    try:
        company_id= (request.GET.get("id", None))
        if(company_id is None):
            return HttpResponse("Please specify the id")
        company_id = int(company_id)
        company_obj_all = list(Company.objects.filter(id=company_id).only('deskripsi'))
        company_obj=Company.objects.filter(id=company_id).first()
        if(company_obj is None):
            return HttpResponse("Sorry, the id you're trying to reach is invalid")
        mulai_invest={}
        mulai_invest['company']=  serializers.serialize('json', company_obj_all)

        mulai_invest['company_photos'] = [i.img.url for i in company_obj.companyphoto_set.all().order_by("img_index")]

        mulai_invest['owner_account']=company_obj.pemilik_usaha.account.user_model.username
        
        company_stock = Stock.objects.filter(company=company_obj)
        lembar_saham_terjual = 0
        for stock in company_stock:
            lembar_saham_terjual += stock.jumlah_lembar_saham

        mulai_invest['saham_terjual']=lembar_saham_terjual
        mulai_invest['saham_tersisa']=company_obj.jumlah_lembar - lembar_saham_terjual
        # pengguna = User.objects.filter(id=)[0]
        # print(request.POST)
        pengguna = UserAccount.objects.filter(id=int(request.GET.get("userId", None)))[0].user_model
        is_exist = Stock.objects.filter(holder=pengguna, company=company_obj)
        if(is_exist.first()):
            mulai_invest['lembar_dimiliki']=is_exist.first().jumlah_lembar_saham
        else:
            mulai_invest['lembar_dimiliki']=0
        return JsonResponse(mulai_invest)
    except:
        return HttpResponse((traceback.format_exc()) +'\n\nrequest.POST = ' + str(request.POST))

@csrf_exempt
def get_saldo(request):
    try:
        userAcc = UserAccount.objects.filter(id=request.GET.get("userId", None))
        userSaldo = userAcc[0].saldo
        return JsonResponse({'saldo':userSaldo})
    except:
        return HttpResponse('fail')

@csrf_exempt
def update_saldo_flutter(request):
    try:
        # if request.method == "POST":
        userId = (request.GET.get('userId', None))
        userAcc = UserAccount.objects.filter(id=userId)
        saldoo = userAcc[0].saldo
        saldo1 = int(saldoo)+int(request.GET.get('saldo', None))
        if saldo1>2000000000:
            return JsonResponse({'message': 'Saldo maksimal Anda adalah 2 miliar Rupiah', 'status': 'fail'})
        if saldo1<0:
            return JsonResponse({'message': 'Saldo minimal adalah 0', 'status': 'fail'})

        obj = userAcc[0]
        obj.saldo=saldo1
        obj.save()

        user = {'id':obj.id,'saldo':obj.saldo, 'status': 'success'}
        return JsonResponse(user)
    except:
        return HttpResponse('fail')

@csrf_exempt
def beli_saham_flutter(request):
    try:
        # if request.method=="POST":
        userId = int(request.GET.get('userId', None))
        userAcc = UserAccount.objects.filter(id=userId)[0]
        saldoo = userAcc.saldo
        saham_dibeli = int(request.GET.get("jumlahLembarSaham"))

        company_id= int(request.GET.get("companyId", None))
        company_obj=Company.objects.filter(id=company_id).first()

        company_stock = Stock.objects.filter(company=company_obj)
        lembar_saham_terjual = 0
        for stock in company_stock:
            lembar_saham_terjual += stock.jumlah_lembar_saham

        sisa_lembar = int(company_obj.jumlah_lembar) - int(lembar_saham_terjual)
        sisa_lembar_after = int(sisa_lembar) - int(saham_dibeli)
        if sisa_lembar_after < 0:
            return JsonResponse({'message': 'Saham yang tersisa pada perusahaan ini hanya ' + str(sisa_lembar) + ' lembar', 'status': 'fail'})

        lembar_saham_terjual += saham_dibeli

        saldo1 = int(saldoo) - int(saham_dibeli) * int(company_obj.nilai_lembar_saham)
        if saldo1 < 0:
            return JsonResponse({'message': 'Saldo Anda tidak cukup :(', 'status': 'fail'})
        
        profile_obj = userAcc
        profile_obj.saldo=saldo1
        profile_obj.save()

        stock_obj = None
        
        pengguna = userAcc.user_model
        is_exist = Stock.objects.filter(holder=pengguna, company=company_obj)
        if(is_exist.first()):
            jumlah_lembar_saham1 = (request.GET.get('jumlahLembarSaham', None))
            stock_obj = is_exist.first()
            jumlah_lembar_saham = int(stock_obj.jumlah_lembar_saham)
            jumlah_lembar_saham+=int(jumlah_lembar_saham1)
            stock_obj.jumlah_lembar_saham=jumlah_lembar_saham
            stock_obj.save()

        else:
            jumlah_lembar_saham1 = int(request.GET.get('jumlahLembarSaham', None))
            stock_obj = Stock.objects.create(
                holder = userAcc,
                company = company_obj,
                jumlah_lembar_saham = jumlah_lembar_saham1
            )

        user = {
            'saldo':profile_obj.saldo, 
            'saham_tersisa': sisa_lembar_after, 
            'saham_tanam': stock_obj.jumlah_lembar_saham,
            'saham_terjual': lembar_saham_terjual,
            'status': 'success'
        }
        return JsonResponse(user)
        # return HttpResponse("hi")
    except:
        return HttpResponse(traceback.format_exc())

@login_required(login_url='/start-web/login')
def mulai_invest(request):
    company_id= (request.GET.get("id", None))
    if(company_id is None):
        return HttpResponse("Please specify the id")
    company_id = int(company_id)
    company_obj=Company.objects.filter(id=company_id).first()
    if(company_obj is None):
        return HttpResponse("Sorry, the id you're trying to reach is invalid")
    mulai_invest={}
    mulai_invest['company']=company_obj
    mulai_invest['company_photos']=company_obj.companyphoto_set.all().order_by("img_index")
    mulai_invest['owner_account']=company_obj.pemilik_usaha.account

    company_stock = Stock.objects.filter(company=company_obj)
    lembar_saham_terjual = 0
    for stock in company_stock:
        lembar_saham_terjual += stock.jumlah_lembar_saham

    mulai_invest['saham_terjual']=lembar_saham_terjual
    mulai_invest['saham_tersisa']=company_obj.jumlah_lembar - lembar_saham_terjual
    
    is_exist = Stock.objects.filter(holder=request.user, company=company_obj)
    if(is_exist.first() is not None):
        mulai_invest['lembar_dimiliki']=is_exist.first().jumlah_lembar_saham
    else:
        mulai_invest['lembar_dimiliki']=0

    return render(request, "mulai_invest.html", mulai_invest)

@login_required(login_url='/start-web/login')
def status_investasi(request):
    user_stock = Stock.objects.filter(holder=request.user)
    response = {'user_stock': user_stock}
    return render(request, 'status_investasi.html', response)
