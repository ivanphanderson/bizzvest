from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.http import HttpResponse
from django.middleware import csrf
from django.shortcuts import render

from halaman_toko.forms.halaman_toko_edit_form import CompanyEditForm
from halaman_toko.forms.halaman_toko_edit_proposal import CompanyAddProposalForm
from halaman_toko.views.utility import validate_toko_id_by_GET_req, validate_toko_id
from models_app.models import Company




def contoh1(req:WSGIRequest):
    return render(req, "HzPyScript/contoh1.html", {
        'variabel_dari_views_py': 'Helloo!! ini adalah HzPyScript, sebuah tag untuk menjalankan program python '
                                   'di template'
    })

