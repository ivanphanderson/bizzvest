import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from halaman_toko.authentication_and_authorization import get_logged_in_user_account


def account_information(req:WSGIRequest):
    logged_in_acc = get_logged_in_user_account(req)
    is_logged_in = logged_in_acc is not None
    is_investor = False
    is_entrepreneur = False

    if is_logged_in:
        is_investor = logged_in_acc.is_investor
        is_entrepreneur = logged_in_acc.is_entrepreneur

    return HttpResponse(
        json.dumps(
            {
                'is_logged_in': int(is_logged_in),
                'is_investor': int(is_investor),
                'is_entrepreneur': int(is_entrepreneur),
            }
        ), status=200
    )


@csrf_exempt
def get_origin(req:WSGIRequest):
    ret = req.META['HTTP_HOST']
    print(ret)
    return HttpResponse(ret, status=200)