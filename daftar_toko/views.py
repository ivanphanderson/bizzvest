from django.shortcuts import render
from django.db.models import Q
from models_app.models import Company
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse
from django.core import serializers
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def tampilkan_toko(request):
    company = Company.objects.all()

    return render(request, 'index_daftar_toko.html', {'company_obj': company})

@csrf_exempt
def search(request):
    company_search = []
    company_list = []
    search_text = ''
    if request.method == "POST":
        search_text = request.POST['search_text']
        company_search = list(Company.objects.filter(Q(nama_perusahaan__icontains=search_text)|Q(nama_merek__icontains=search_text)|Q(kode_saham__icontains=search_text)).values())       
    else:
        company_search = list(Company.objects.all().values())

    for company in company_search:
        if Company.objects.get(id=company["id"]).status_verifikasi == 3:
            company["img"] = Company.objects.get(id=company["id"]).companyphoto_set.all().order_by('img_index').first().img.url
            company_list.append(company)

    return JsonResponse({'company_search' : company_list})


@csrf_exempt
def searchMobile(request):
    company_search = []
    company_list = []
    search_text = ''
    if request.method == "POST":
        data = json.loads(request.body)
        search_text = data['search_text']
        company_search = list(Company.objects.filter(Q(nama_perusahaan__icontains=search_text)|Q(nama_merek__icontains=search_text)|Q(kode_saham__icontains=search_text)).values())       
    else:
        company_search = list(Company.objects.all().values())

    for company in company_search:
        if Company.objects.get(id=company["id"]).status_verifikasi == 3:
            company["img"] = Company.objects.get(id=company["id"]).companyphoto_set.all().order_by('img_index').first().img.url
            company_list.append(company)

    return JsonResponse({'company_search' : company_list})

