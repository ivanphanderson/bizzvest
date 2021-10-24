from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.middleware import csrf
from django.shortcuts import render

from halaman_toko.forms.halaman_toko_edit_form import CompanyEditForm
from halaman_toko.views.utility import validate_toko_id_by_GET_req
from models.models import Company




class InformasiSaham():
    def __init__(self, company:Company):
        self.lembar_saham_terjual = company.stock_set.aggregate(result=Sum('jumlah_lembar_saham'))['result']

        if self.lembar_saham_terjual is None:
            self.lembar_saham_terjual = 0

        self.total_saham_terjual = self.lembar_saham_terjual * company.nilai_lembar_saham
        self.persentase_terjual = round(100 * self.lembar_saham_terjual / company.jumlah_lembar, 1)
        self.persentase_terjual_int = round(self.persentase_terjual)

        self.lembar_saham_tersisa = company.jumlah_lembar - self.lembar_saham_terjual
        self.total_saham_tersisa = self.lembar_saham_tersisa * company.nilai_lembar_saham
        self.persentase_tersisa = 100 - self.persentase_terjual



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
        'informasi_saham': InformasiSaham(company_obj),
    })