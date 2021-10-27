from django.shortcuts import render
from models_app.models import Company
# Create your views here.

def tampilkan_toko(request):
    context = {}
    return render(request, 'index_daftar_toko.html')