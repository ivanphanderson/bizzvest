from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

# from halaman_toko.forms.halaman_toko_edit_form import CompanyEditForm
from django.middleware import csrf
from django.db.models import Sum
from models_app.models.UserAccount import UserAccount

# from mulai_invest.models import Profile
# from .forms import ExtendedUserForm, ProfileForm, StockForm, CreateUserForm
from django.contrib import messages

from models_app.models import Company
from models_app.models import Stock
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import View
# Create your views here.
# a=None

# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect('/mulai-invest/')
#     else:
#         # form = CreateUserForm()
#         # profile_form = ProfileForm()
#         if request.method == 'POST':
#             form = ExtendedUserForm(request.POST)
#             profile_form=ProfileForm(request.POST)
#             if form.is_valid() and profile_form.is_valid():
#                 user = form.save()
#                 profile=profile_form.save(commit=False)
#                 profile.user=user

#                 profile.save()

#                 user = form.cleaned_data.get('username')
#                 messages.success(request, 'Account was created for ' + user)
                
#                 return redirect('login')
#         else:
#             form=ExtendedUserForm()
#             profile_form=ProfileForm()
#         context = {'form':form, 'profile_form': profile_form}
#         return render(request, 'register.html', context)

# def loginPage(request):
# 	if request.user.is_authenticated:
# 		return redirect('/mulai-invest/')
# 	else:
# 		if request.method == 'POST':
# 			username = request.POST.get('username')
# 			password = request.POST.get('password')

# 			user = authenticate(request, username=username, password=password)

# 			if user is not None:
# 				login(request, user)
# 				return redirect('/mulai-invest/?id=1')
# 			else:
# 				messages.info(request, 'Username OR password is incorrect')

# 		context = {}
# 		return render(request, 'logins.html', context)

# def logoutUser(request):
#     logout(request)
#     return redirect('login')

def go_to_prev_history_javascript(time_in_ms):
    ret = """
    <script>
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        (
            async function (){
                await sleep( """ + str(time_in_ms) + """);
                window.history.go(-1);
            }
        )();
    </script>
    """
    return ret

class UpdateSaldo(View):
    def  get(self, request):
        # name1 = request.user
        saldoo = request.user.useraccount.saldo
        saldo1 = int(saldoo)+int(request.GET.get('saldo', None))
        # print(saldo1)

        obj = get_object_or_404(UserAccount, user_model=request.user)
        obj.saldo=saldo1
        print(saldo1)
        # obj.name=name1
        obj.save()

        user = {'id':obj.id,'saldo':obj.saldo}


        data = {
            'user': user
        }
        return JsonResponse(data)


class BeliSaham(View):
    def  get(self, request):
        #  if request.is_ajax and request.method == "GET":
        # print(request.GET.get('saldo', None))
        saldo1 = int(request.GET.get("saldo", None))
        company_id= int(request.GET.get("id", None))
        company_obj=Company.objects.filter(id=company_id).first()
        
        
        print(saldo1)
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


def halaman_toko(request):
    # is_valid, ret_obj = validate_toko_id_by_GET_req(req)
    # if not is_valid:
    #     return ret_obj
    company_id= (request.GET.get("id", None))
    if(company_id is None):
        return HttpResponse("Please specify the id")
    company_id = int(company_id)
    company_obj=Company.objects.filter(id=company_id).first()
    if(company_obj is None):
        return HttpResponse("Sorry, the id you're trying to reach is invalid")
    # company_obj:Company = ret_obj[0]
    mulai_invest={}
    mulai_invest['company']=company_obj
    mulai_invest['company_photos']=company_obj.companyphoto_set.all().order_by("img_index")
    mulai_invest['owner_account']=company_obj.pemilik_usaha.account
    # print(mulai_invest['owner_account'].user_model.username)
    
    company_stock = Stock.objects.filter(company=company_obj)
    lembar_saham_terjual = 0
    # lembar_saham_terjual = company_obj.stock_set.aggregate(result=Sum('jumlah_lembar_saham'))['result']
    for stock in company_stock:
        lembar_saham_terjual += stock.jumlah_lembar_saham
    print(lembar_saham_terjual)

    mulai_invest['saham_terjual']=lembar_saham_terjual
    mulai_invest['saham_tersisa']=company_obj.jumlah_lembar - lembar_saham_terjual
    
    is_exist = Stock.objects.filter(holder=request.user, company=company_obj)
    if(is_exist.first() is not None):
        mulai_invest['lembar_dimiliki']=is_exist.first().jumlah_lembar_saham
    else:
        mulai_invest['lembar_dimiliki']=0
    # form = StockForm(req.POST or None)
    # form.instance.holder=req.user
    # form.instance.company=company_obj
    

    # # id_comp=req.GET.get("id")
    # cdf = Stock.objects.filter(holder=req.user, company=company_obj)
    # if (cdf.first() is not None):
    #     print(cdf)
    #     print("tes")
    #     obj = get_object_or_404(Stock, holder=req.user,company=company_obj)
    #     print(obj)
    # else:
        
    # ghi = Stock.objects.filter(company=company_obj)
    # mulai_invest["note"] = req.id
    
    # print(req.user.profile.saldo)
    # print(cdf)
    # print(ghi)

    

    # if(form.is_valid() and req.method == 'POST'):
    #     saved_obj:Stock = form.save()
    #     return HttpResponseRedirect("#")
    
    # mulai_invest['form']=form

    return render(request, "mulai_invest.html", mulai_invest)

def validate_toko_id_by_GET_req(req:WSGIRequest):
    "returns (True, company_obj_query) if valid, or (False, http response object) if is not valid"
    if (req.GET.get("id") is None):
        ret = HttpResponseRedirect("")
        ret["Location"] += "?id=1"
        return (False, ret)

    return validate_toko_id(req.GET.get("id"))



def validate_toko_id(id_str:str):
    "returns (True, company_obj_query) if valid, or (False, http response object) if is not valid"
    company_id_str:str = id_str
    if (not company_id_str.isnumeric()):
        ret = HttpResponse("Sorry, the id you're trying to reach is invalid " + go_to_prev_history_javascript(3000))
        ret.status_code = 400
        return (False, ret)

    company_id:int = int(company_id_str)
    company_obj_query = Company.objects.filter(id=company_id)
    if (not company_obj_query.exists()):
        ret = HttpResponse("Sorry, the id you're trying to reach does not exist " + go_to_prev_history_javascript(3000))
        ret.status_code = 400
        return (False, ret)
    return (True, company_obj_query)