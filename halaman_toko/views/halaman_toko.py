from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.http import HttpResponse
from django.middleware import csrf
from django.shortcuts import render

from halaman_toko.forms.halaman_toko_edit_form import CompanyEditForm
from halaman_toko.forms.halaman_toko_edit_proposal import CompanyAddProposalForm
from halaman_toko.views.utility import validate_toko_id_by_GET_req, validate_toko_id
from models_app.models import Company




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
        'StatusVerifikasi': Company.StatusVerifikasi,
        'company_photos': company_obj.companyphoto_set.all().order_by("img_index"),
        'edit_form': CompanyEditForm(None),
        'django_csrf_token': csrf.get_token(req),
        'owner_account': company_obj.pemilik_usaha.account,
        'informasi_saham': InformasiSaham(company_obj),
    })



def edit_proposal(req:WSGIRequest):
    if req.method != 'POST':
        return HttpResponse(status=400)

    if 'company_id' not in req.POST:
        return HttpResponse('Field does not exist: company_id', status=400)

    is_valid, ret_obj = validate_toko_id(req.POST['company_id'])
    if not is_valid:
        return ret_obj

    if req.FILES.get('proposal', None) is None:
        return HttpResponse('Proposal must be submitted', status=400)

    company_obj:Company = ret_obj[0]
    # TODO: authentication and authorization

    form = CompanyAddProposalForm(req, req.FILES, instance=company_obj)

    if (form.is_valid()):
        form.save()
        form_instance:Company = form.instance
        return HttpResponse(form_instance.proposal.url, status=200)

    try:
        return HttpResponse(
            # harusnya cuman ada 1 field yang error, karena memang cuman ada 1 field
            form.errors.as_data()['proposal'][-1].message,
            status=400
        )
    except:
        return HttpResponse(str(form.errors), status=400)

def proposal_not_available(req:WSGIRequest):
    return HttpResponse("This company hasn't uploaded any proposal yet.", status=404)



def save_company_form(req:WSGIRequest):
    if (req.method != 'POST'):
        return HttpResponse('invalid request: not a POST request', status=400)

    if (temp:=is_available('deskripsi', req.POST)) is not True:
        return temp

    if (temp:=is_available('id', req.POST)) is not True:
        return temp

    # TODO: authentication and authorization
    id = req.POST['id']

    is_company_valid, obj = validate_toko_id(id)
    if not is_company_valid:
        return obj

    company_object = obj.first()  # get the first query. I think it should only have one item tho
    if (company_object.status_verifikasi != Company.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI):
        return HttpResponse("verification status must be 'not submitted yet' to alter any information", status=400)

    form = CompanyEditForm(req.POST, instance=company_object)

    if (form.is_valid()):
        print(form)
        form.save()
        return HttpResponse('saved successfully!', status=200)
    else:
        assert form.errors
        error_messages = []
        for field, error in form.errors.items():
            error_messages.append(f"{field}  {str(error.as_data()[0])}")
        return HttpResponse('the following errors has occured: \n\n ' + '\n'.join(error_messages), status=400)


def ajukan_verifikasi(req:WSGIRequest):
    if (req.method != 'POST'):
        return HttpResponse('invalid request: not a POST request', status=400)

    if (temp:=is_available('id', req.POST)) is not True:
        return temp
    # TODO: authentication and authorization

    id = req.POST['id']

    is_valid, obj = validate_toko_id(id)
    if not is_valid:
        return obj

    company_object:Company = obj[0]

    if (company_object.status_verifikasi != Company.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI):
        return HttpResponse("Invalid verification status", status=400)

    if (not company_object.proposal):
        return HttpResponse("Proposal must be uploaded", status=400)

    if (company_object.companyphoto_set.all().count() == 0):
        return HttpResponse("The company must have at least 1 photo", status=400)


    company_object.status_verifikasi = Company.StatusVerifikasi.MENGAJUKAN_VERIFIKASI
    company_object.save()

    return HttpResponse("success!")


def is_available(field_name:str, request_query:dict):
    if (field_name not in request_query):
        return HttpResponse(f'invalid request: {repr(field_name)} field is not available', status=400)
    return True