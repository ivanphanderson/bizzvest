from typing import Union

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.urls import reverse

from models_app.models.UserAccount import *




def get_logged_in_user_account(req:WSGIRequest) -> Union[UserAccount, None]:
    "Mengembalikan object UserAccount jika pengunjung saat ini sudah login, atau None jika belum login (guest user)"

    if not req.user.is_authenticated:
        return None

    return req.user.useraccount



def get_login_url() -> str:

    # TO DO: Arahkan kepada login page yang sesungguhnya setelah Tito menyelesaikan login system-nya
    return reverse('login')
    # return "/admin"



