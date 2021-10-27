from django.shortcuts import render
from models_app.models import Company
from halaman_toko.views.utility import validate_toko_id_by_GET_req, validate_toko_id

# Create your views here.

def tampilkan_toko(request):
    company = Company.objects.all().values()
    company_obj = Company.objects.all()
    return render(request, 'index_daftar_toko.html', {'company': company, 'company_obj': company_obj})

def insert_photos_dict():
    company = Company.objects.all()