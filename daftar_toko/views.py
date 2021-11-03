from django.shortcuts import render
from django.db.models import Q
from models_app.models import Company
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse
from django.core import serializers
from django.template.context_processors import csrf

# Create your views here.

def tampilkan_toko(request):
    company = Company.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(company, 6)
    try:
        company_obj = paginator.page(page)
    except PageNotAnInteger:
        company_obj = paginator.page(1)
    except EmptyPage:
        company_obj = paginator.page(paginator.num_pages)

    return render(request, 'index_daftar_toko.html', {'company_obj': company_obj})

def search(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    company_search = Company.objects.filter(nama_perusahaan__contains=search_text, nama_merek__contains=search_text)

    return render(request, 'search.html', {'company_obj' : company_search})

def experiment(request):
    data = serializers.serialize('json', Company.objects.all())
    return HttpResponse(data, content_type="application/json")
