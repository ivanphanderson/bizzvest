import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from halaman_toko.authentication_and_authorization import *
from halaman_toko.forms.halaman_toko_add_foto import CompanyPhotoAddForm
from halaman_toko.views.utility import validate_toko_id_by_GET_req, validate_toko_id
from models_app.models import Company, CompanyPhoto
from models_app.models_utility.company_utility import recalculate_img_index, recalculate_img_index_from_list



@csrf_exempt
def photo_json(req:WSGIRequest):
    if 'id' not in req.GET:
        return HttpResponse("field not found: id", status=400)

    is_toko_id_valid, object = validate_toko_id(req.GET['id'])
    if not is_toko_id_valid:
        return object

    company:Company = object[0]
    temp = get_photos_json(company)
    return temp



def add_photo(req:WSGIRequest):
    if (get_logged_in_user_account(req) is None):
        return HttpResponseRedirect(get_login_url())

    if (req.method == 'POST'):
        if 'company_id' not in req.POST:
            return HttpResponse("field not found: company_id", status=400)

        if 'img' not in req.FILES:
            return HttpResponse("field not found: img", status=400)

        is_toko_id_valid, object = validate_toko_id(req.POST['company_id'])
        if not is_toko_id_valid:
            return object

        company:Company = object[0]
        user_object = get_logged_in_user_account(req)
        if user_object is None:
            return HttpResponse('please log in', status=403)
        if user_object.user_model.username != company.pemilik_usaha.account.user_model.username:
            return HttpResponse('you are not the owner of this company', status=403)

        if (company.status_verifikasi != Company.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI):
            return HttpResponse("Verification status must be 'not submitted yet' to alter any photo", status=400)


        company_photos_count = company.companyphoto_set.all().count()

        if (company_photos_count + len(req.FILES.getlist('img')) > 12):
            return HttpResponse("Sorry, you can't add any photo more than 12", status=400)

        uploaded_images = req.FILES.getlist("img")  # daftar semua file yang di upload oleh <input type="file" multiple>

        for i in range(len(uploaded_images)):
            files_temp = req.FILES.copy()
            files_temp.setlist(
                'img',
                [ req.FILES.getlist('img')[i], ]
            )


            form = CompanyPhotoAddForm(req.POST, files_temp)
            form.instance.img_index = company_photos_count + 1
            company_photos_count += 1
            form.instance.company = company


            if (form.is_valid()):
                saved_obj:CompanyPhoto = form.save()
            else:
                return HttpResponse("Sorry, the form you've given is invalid. <!--" + str(form.errors) + "-->", status=400)
        return get_photos_json(company)
    return HttpResponse("Invalid request", status=400)


def delete_photo(req:WSGIRequest):
    if (get_logged_in_user_account(req) is None):
        return HttpResponseRedirect(get_login_url())

    if (req.method == 'POST'):
        if not 'photo_id' in req.POST:
            return HttpResponse("field not found: photo_id", status=400)

        photo_id_str:str = req.POST['photo_id']
        if not photo_id_str.isnumeric():
            return HttpResponse("non numeric: photo_id", status=400)

        photo_id:int = int(photo_id_str)
        object = CompanyPhoto.objects.filter(id=photo_id).first()
        if (object is None):
            return HttpResponse("photo_id object is not found", status=400)

        photo_obj:CompanyPhoto = object
        photo_index = photo_obj.img_index
        company_obj:Company = photo_obj.company
        user_object = get_logged_in_user_account(req)
        if user_object is None:
            return HttpResponse('please log in', status=403)
        if user_object.user_model.username != company_obj.pemilik_usaha.account.user_model.username:
            return HttpResponse('you are not the owner of this company', status=403)

        if (company_obj.status_verifikasi != Company.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI):
            return HttpResponse("Verification status must be 'not submitted yet' to alter any photo", status=400)

        company_photos = list(company_obj.companyphoto_set.all().order_by('img_index'))
        photo_index_in_the_list = photo_index-1
        assert (company_photos[photo_index_in_the_list].id == photo_obj.id), \
            "img_index tidak sesuai dengan posisinya pada array"  # +1 because img_index is starts from 1

        company_photos[photo_index_in_the_list].delete()
        recalculate_img_index(company_obj, photo_index_in_the_list)

        temp = get_photos_json(company_obj)
        return temp
    return HttpResponse("Invalid request", status=400)


def photo_reorder(req:WSGIRequest):
    if (get_logged_in_user_account(req) is None):
        return HttpResponseRedirect(get_login_url())

    if (req.method == 'POST'):
        if not 'photo_order' in req.POST:
            return HttpResponse("field not found: photo_order", status=400)

        is_company_valid, object = validate_toko_id(req.POST['company_id'])
        if not is_company_valid:
            return object
        
        company:Company = object.first()
        user_object = get_logged_in_user_account(req)
        if user_object is None:
            return HttpResponse('please log in', status=403)
        if user_object.user_model.username != company.pemilik_usaha.account.user_model.username:
            return HttpResponse('you are not the owner of this company', status=403)

        if (company.status_verifikasi != Company.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI):
            return HttpResponse("Verification status must be 'not submitted yet' to alter any photo", status=400)

        photo_order_json_string = req.POST['photo_order']
        try:
            photo_order = json.loads(photo_order_json_string)
            if not isinstance(photo_order, dict):
                return HttpResponse("invalid json [not a dict]: photo_order  ", status=400)
            for key, value in photo_order.items():
                if not key.isnumeric():
                    return HttpResponse("invalid json [non-numeric dict key]: photo_order", status=400)
                if not isinstance(value, int) or not (0 <= value < 1000):
                    return HttpResponse("invalid json [invalid dict value]: photo_order", status=400)
        except ValueError as e:
            return HttpResponse("invalid json: photo_order", status=400)

        for key,value in set(photo_order.items()):
            photo_order[int(key)] = value
            del photo_order[key]  # delete the string version of the key

        if (company.companyphoto_set.all().count() != len(photo_order)):
            return HttpResponse("invalid json [non-equal length]: photo_order", status=400)

        company_photos = list(company.companyphoto_set.all())

        for company_photo in company_photos:
            if company_photo.id not in photo_order:
                return HttpResponse("invalid json [non-equal dict]: photo_order", status=400)

        for company_photo in company_photos:
            company_photo.img_index = photo_order[company_photo.id]

        company_photos.sort(key=lambda x: x.img_index)

        # normalisasi. Pakai fungsi ini, karena siapa tahu ada orang iseng atau hacker sialan yg berusaha
        # membuat img_index kacau. (img_index dikatakan kacau kalau ga dimulai dari 1 atau kalau ada bolongnya,
        # misalnya [1, 3, 2, 7, 5, 6] ada bolongnya: img_index 4 tidak ditemukan)
        recalculate_img_index_from_list(company_photos)  # sudah termasuk menyimpan urutan ke database

        return HttpResponse("success", status=200)
    return HttpResponse("Invalid request", status=400)


def manage_photos(req:WSGIRequest, *args, **kwargs):
    if req.method == "GET":
        is_valid, ret_obj = validate_toko_id_by_GET_req(req)
        if not is_valid:
            return ret_obj

        company_obj:Company = ret_obj[0]
        user_object = get_logged_in_user_account(req)
        if user_object is None:
            return HttpResponse('please log in', status=403)
        if user_object.user_model.username != company_obj.pemilik_usaha.account.user_model.username:
            return HttpResponse('you are not the owner of this company', status=403)

        if "ajax_get_json" in req.GET:
            return get_photos_json(company_obj)

        return render(req, "manage_photos.html", {
            'company': company_obj
        })



def get_photos_json(company_obj):
    company_photos = company_obj.companyphoto_set.all().order_by('img_index')

    return HttpResponse(
        json.dumps(
            [{
                'id': img.id,
                'url': img.img.url
            }
                for img in company_photos]
    ), content_type='application/json')
