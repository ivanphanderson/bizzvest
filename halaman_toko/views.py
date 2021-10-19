from django.urls import reverse
from django.core import serializers
from django.core.exceptions import ValidationError
from django.middleware import csrf
from django.utils import dateformat

from halaman_toko.authentication_and_authorization import *
from halaman_toko.forms.halaman_toko_add_form import CompanyAddForm
from halaman_toko.forms.halaman_toko_edit_form import CompanyEditForm
from models.models.Company import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

# Create your views here.

def go_to_prev_history_javascript(time_in_ms):
    ret = """
    <script>
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        (
            async function (){
                await sleep( """ + str(time_in_ms) + """);
                window.history.go(-1);
            }
        )();
    </script>
    """
    return ret


def validate_toko_id_by_GET_req(req:WSGIRequest):
    "returns (True, company_obj_query) if valid, or (False, http response object) if is not valid"
    if (req.GET.get("id") is None):
        ret = HttpResponseRedirect("")
        ret["Location"] += "?id=1"
        return (False, ret)

    return validate_toko_id(req.GET.get("id"))



def validate_toko_id(id_str:str):
    "returns (True, company_obj_query) if valid, or (False, http response object) if is not valid"
    company_id_str:str = id_str
    if (not company_id_str.isnumeric()):
        ret = HttpResponse("Sorry, the id you're trying to reach is invalid " + go_to_prev_history_javascript(3000))
        ret.status_code = 400
        return (False, ret)

    company_id:int = int(company_id_str)
    company_obj_query = Company.objects.filter(id=company_id)
    if (not company_obj_query.exists()):
        ret = HttpResponse("Sorry, the id you're trying to reach is not exist " + go_to_prev_history_javascript(3000))
        ret.status_code = 400
        return (False, ret)
    return (True, company_obj_query)



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
    })




def add_toko(req:WSGIRequest):

    validation_state = '1'
    show_invalid_modal = False
    additional_problems = []

    if (get_logged_in_user_account() is None):
        return HttpResponseRedirect(get_login_url())


    if (req.method == 'POST'):
        form = CompanyAddForm(req.POST)
        print(timezone.now())
        form.instance.start_date = dateformat.format(timezone.now(), 'Y-m-d')

        temp = get_logged_in_user_account().entrepreneuraccountdata
        form.instance.pemilik_usaha = temp
        print(temp)

        # if ('pemilik_usaha' in req.POST):
        #     return HttpResponse("Illegal attribute: 'pemilik_usaha' ", status=400)

        if ('is_validate_only' not in req.POST):
            additional_problems.append("invalid request error: no 'is_validate_only' property")
            show_invalid_modal = True
        else:
            if (form.is_valid()):
                print("form valid")
                if (req.POST.get('is_validate_only', '1') == '0'):
                    saved_obj:Company = form.save()
                    print("saved")

                    redirect_url_target = reverse('halaman_toko:halaman_toko')
                    return HttpResponseRedirect(f"{redirect_url_target}?id={saved_obj.id}")
                elif req.POST['is_validate_only'] == '1':
                    validation_state = '0'
            else:
                print("form invalid")
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







def manage_photos(req:WSGIRequest):
    if req.method == "GET":
        is_valid, ret_obj = validate_toko_id_by_GET_req(req)
        if not is_valid:
            return ret_obj


        # TODO: authentication and authorization

        company_obj:Company = ret_obj[0]
        company_photos = company_obj.companyphoto_set.all()

        if "ajax_get_json" in req.GET:
            print("asdfgh")
            return HttpResponse(serializers.serialize('json', company_photos), content_type='application/json')

        return render(req, "manage_photos.html", {
            'company': company_obj
        })

    elif req.method == "POST":
        pass



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

    if not (temp:=validate_toko_id(id))[0]:
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





def dummy(req):
    return render(req, "tes.html", {})