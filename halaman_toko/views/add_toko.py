import json

from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse
from django.middleware import csrf
from django.shortcuts import render
from django.urls import reverse
from django.utils import dateformat, timezone

from halaman_toko.authentication_and_authorization import *
from halaman_toko.forms.halaman_toko_add_form import CompanyAddForm
from models_app.models import Company, EntrepreneurAccount


class DoesProblemExist():
    def __init__(self):
        pass


class FormErrors():
    def __init__(self, errors):
        # dictionary = dict(errors)
        dictionary = errors.as_data()
        fields_list =  ['proposal',
                        'nama_merek',
                        'nama_perusahaan',
                        'alamat',
                        'deskripsi',
                        'jumlah_lembar',
                        'nilai_lembar_saham',
                        'kode_saham',
                        'dividen',
                        'end_date',
                        ]

        self.does_problem_exist = DoesProblemExist()

        no_error = (ValidationError("") ,)
        for attr_name in fields_list:
            temp:ValidationError = dictionary.get(attr_name, no_error)[-1]
            setattr(self, attr_name, temp.message)
            setattr(self.does_problem_exist, attr_name, "problem" if (attr_name in dictionary) else "no-problem")



def add_toko(req:WSGIRequest):
    # TemporaryFiles.delete_outdated_files()

    validation_state = '1'
    show_invalid_modal = False
    additional_problems = []

    logged_in_account = get_logged_in_user_account(req)
    if (logged_in_account is None):
        return HttpResponseRedirect(get_login_url())

    if (req.method == 'POST'):
        form = CompanyAddForm(req.POST)
        form.instance.start_date = dateformat.format(timezone.now(), 'Y-m-d')

        if ('pemilik_usaha' in req.POST):
            return HttpResponse("Illegal attribute: 'pemilik_usaha' ", status=400)

        if not logged_in_account.is_entrepreneur:
            logged_in_account.entrepreneuraccount = EntrepreneurAccount(account=logged_in_account)
            logged_in_account.entrepreneuraccount.save()
            logged_in_account.save()

        temp = logged_in_account.entrepreneuraccount
        form.instance.pemilik_usaha = temp


        if ('is_validate_only' not in req.POST):
            additional_problems.append("invalid request error: no 'is_validate_only' property")
            show_invalid_modal = True
        else:
            if (form.is_valid()):
                if req.POST.get('is_validate_only', '1') == '0':
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
                                      for field_name, errors in form.errors.items()],
        'errors': FormErrors(form.errors),
    })



def add_toko_API(req:WSGIRequest):
    additional_problems = []

    logged_in_account = get_logged_in_user_account(req)
    if (logged_in_account is None):
        return HttpResponseRedirect(get_login_url())

    if (req.method == 'POST'):
        form = CompanyAddForm(req.POST)
        form.instance.start_date = dateformat.format(timezone.now(), 'Y-m-d')

        if 'pemilik_usaha' in req.POST:
            return HttpResponse("Illegal attribute: 'pemilik_usaha' ", status=400)

        if not logged_in_account.is_entrepreneur:
            logged_in_account.entrepreneuraccount = EntrepreneurAccount(account=logged_in_account)
            logged_in_account.entrepreneuraccount.save()
            logged_in_account.save()

        temp = logged_in_account.entrepreneuraccount
        form.instance.pemilik_usaha = temp


        if ('is_validate_only' not in req.POST):
            additional_problems.append("invalid request error: no 'is_validate_only' property")
        else:
            if (form.is_valid()):
                if (req.POST.get('is_validate_only', '1') == '0'):
                    saved_obj:Company = form.save()
                    return HttpResponse(
                        json.dumps({
                            'id': saved_obj.id,
                        }), content_type="application/json"
                    )
                elif req.POST['is_validate_only'] == '1':
                    return HttpResponse(
                        json.dumps({
                            'is_valid': 1,
                            'csrftoken': csrf.get_token(req),
                            'errors': []
                        }), content_type="application/json"
                    )

            resulting_err_dict = {}

            err_dicts = form.errors.as_data()
            fields_list =  ['proposal',
                            'nama_merek',
                            'nama_perusahaan',
                            'alamat',
                            'deskripsi',
                            'jumlah_lembar',
                            'nilai_lembar_saham',
                            'kode_saham',
                            'dividen',
                            'end_date',
                            ]

            for attr_name in fields_list:
                iterable_temp: list[ValidationError] = err_dicts.get(attr_name, [])
                if not iterable_temp:
                    continue
                resulting_err_dict[attr_name] = []
                for i in iterable_temp:
                    resulting_err_dict[attr_name].append(i.message)
            print(resulting_err_dict)
            print()
            print()

            return HttpResponse(
                json.dumps({
                    'is_valid': 0,
                    'csrftoken': csrf.get_token(req),
                    'errors': resulting_err_dict
                }), status=422, content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({
                'is_valid': -1,
                'csrftoken': csrf.get_token(req),
                'errors': []
            }), content_type="application/json"
        )



