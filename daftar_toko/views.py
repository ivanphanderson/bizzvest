from django.shortcuts import render
from django.db.models import Q
from models_app.models import Company
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse
from django.core import serializers
from django.views.generic import ListView

# Create your views here.

def tampilkan_toko(request):
    company_obj = Company.objects.all()

    return render(request, 'index_daftar_toko.html', {'company_obj': company_obj})

def search(request):
    company_search = []
    search_text = ''
    if request.method == "POST":
        search_text = request.POST['search_text']
        company_search = list(Company.objects.filter(Q(nama_perusahaan__contains=search_text)|Q(nama_merek__contains=search_text)|Q(kode_saham__contains=search_text)).values())       
    else:
        company_search = list(Company.objects.all().values())
    
    for company in company_search:
        company["img"] = Company.objects.get(id=company["id"]).companyphoto_set.all().order_by('img_index').first().img.url

    return JsonResponse({'company_search' : company_search})

def experiment(request):
    data = serializers.serialize('json', Company.objects.all())
    return HttpResponse(data, content_type="application/json")

