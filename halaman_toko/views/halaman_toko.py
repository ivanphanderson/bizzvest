from django.core.handlers.wsgi import WSGIRequest
from django.middleware import csrf
from django.shortcuts import render

from halaman_toko.forms.halaman_toko_edit_form import CompanyEditForm
from halaman_toko.views.utility import validate_toko_id_by_GET_req
from models.models import Company


def halaman_toko(req:WSGIRequest):
    is_valid, ret_obj = validate_toko_id_by_GET_req(req)
    if not is_valid:
        return ret_obj

    company_obj:Company = ret_obj[0]

    return render(req, "halaman_toko.html", {
        'company': company_obj,
        'company_photos': company_obj.companyphoto_set.all().order_by("img_index"),
        'edit_form': CompanyEditForm(None),
        'django_csrf_token': csrf.get_token(req),
        'owner_account': company_obj.pemilik_usaha.account,
    })