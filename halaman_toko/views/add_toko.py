from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import dateformat, timezone

from halaman_toko.authentication_and_authorization import get_logged_in_user_account, get_login_url
from halaman_toko.forms.halaman_toko_add_form import CompanyAddForm
from halaman_toko.forms.halaman_toko_edit_form import CompanyEditForm
from halaman_toko.views.utility import validate_toko_id
from models.models import Company


def add_toko(req:WSGIRequest):

    validation_state = '1'
    show_invalid_modal = False
    additional_problems = []

    if (get_logged_in_user_account() is None):
        return HttpResponseRedirect(get_login_url())


    if (req.method == 'POST'):
        form = CompanyAddForm(req.POST)
        form.instance.start_date = dateformat.format(timezone.now(), 'Y-m-d')

        temp = get_logged_in_user_account().entrepreneuraccount
        form.instance.pemilik_usaha = temp

        # if ('pemilik_usaha' in req.POST):
        #     return HttpResponse("Illegal attribute: 'pemilik_usaha' ", status=400)

        if ('is_validate_only' not in req.POST):
            additional_problems.append("invalid request error: no 'is_validate_only' property")
            show_invalid_modal = True
        else:
            if (form.is_valid()):
                if (req.POST.get('is_validate_only', '1') == '0'):
                    saved_obj:Company = form.save()

                    redirect_url_target = reverse('halaman_toko:halaman_toko')
                    return HttpResponseRedirect(f"{redirect_url_target}?id={saved_obj.id}")
                elif req.POST['is_validate_only'] == '1':
                    validation_state = '0'
            else:
                show_invalid_modal = True
    else:
        form = CompanyAddForm(None)

    return render(req, "add_toko.html", {
        'form':form,
        'validation_state': validation_state,
        'additional_problems': additional_problems,
        'show_invalid_modal': show_invalid_modal,
        'errors_field_verbose_name': [Company._meta.get_field(field_name).verbose_name
                                      for field_name, errors in form.errors.items()]
    })


def is_available(field_name:str, request_query:dict):
    if (field_name not in request_query):
        return HttpResponse(f'invalid request: {repr(field_name)} field is not available', status=400)
    return True


def save_company_form(req:WSGIRequest):
    if (req.method != 'POST'):
        return HttpResponse('invalid request: not a POST request', status=400)

    if (temp:=is_available('deskripsi', req.POST)) is not True:
        return temp
    if (temp:=is_available('id', req.POST)) is not True:
        return temp

    # TODO: authentication and authorization
    id = req.POST['id']

    if not (temp:= validate_toko_id(id))[0]:
        return temp[1]
    # validate_toko_id() returns (True, company_obj_query) when valid, or (False, HttpResponse) when invalid
    company_object_query = temp[1]
    company_object = company_object_query[0]  # get the first query. I think it should only have one item tho
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