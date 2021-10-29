from django.shortcuts import render
from django.db.models import Q
from models_app.models import Company
from halaman_toko.views.utility import validate_toko_id_by_GET_req, validate_toko_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    query = request.GET.get('q')
    if query is not None and query != '' and request.is_ajax():
        company_obj = Company.objects.filter(  
            Q(title__icontains=query)
        )

        return render(request, '/snippets/index_daftar_toko.html', {'company_obj': company_obj})
    return render(request, '/snippets/index_daftar_toko.html')

