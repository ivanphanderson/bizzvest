from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from models_app.models.UserAccount import UserAccount
from models_app.models import Company
from models_app.models import Stock
# Create your views here.

class UpdateSaldo(View):
    def  get(self, request):
        saldoo = request.user.useraccount.saldo
        saldo1 = int(saldoo)+int(request.GET.get('saldo', None))

        obj = get_object_or_404(UserAccount, user_model=request.user)
        obj.saldo=saldo1
        obj.save()

        user = {'id':obj.id,'saldo':obj.saldo}


        data = {
            'user': user
        }
        return JsonResponse(data)


class BeliSaham(View):
    def  get(self, request):
        saldo1 = int(request.GET.get("saldo", None))
        company_id= int(request.GET.get("id", None))
        company_obj=Company.objects.filter(id=company_id).first()
        
        
        profile_obj = get_object_or_404(UserAccount, user_model=request.user)
        profile_obj.saldo=saldo1
        profile_obj.save()
        
        is_exist = Stock.objects.filter(holder=request.user, company=company_obj)
        if(is_exist.first() is not None):
            
            jumlah_lembar_saham1 = (request.GET.get('jumlah_lembar_saham', None))
            stock_obj = get_object_or_404(Stock, holder=request.user,company=company_obj)
            jumlah_lembar_saham = int(stock_obj.jumlah_lembar_saham)
            jumlah_lembar_saham+=int(jumlah_lembar_saham1)
            stock_obj.jumlah_lembar_saham=jumlah_lembar_saham
            stock_obj.save()

        else:
            jumlah_lembar_saham1 = int(request.GET.get('jumlah_lembar_saham', None))
            stock_obj = Stock.objects.create(
                holder = request.user,
                company = company_obj,
                jumlah_lembar_saham = jumlah_lembar_saham1
            )

        user = {'id':profile_obj.id,'saldo':profile_obj.saldo}

        data = {
            'user': user
        }
        return JsonResponse(data)

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
