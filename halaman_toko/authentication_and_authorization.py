from typing import Union

from django.db.models import QuerySet
from models.models.UserAccount import *




def get_logged_in_user_account() -> Union[UserAccount, None]:
    "Mengembalikan object UserAccount jika pengunjung saat ini sudah login, atau None jika belum login (guest user)"

    # TODO: Implementasikan method ini secara sesungguhnya setelah Tito menyelesaikan login system-nya
    ret:QuerySet = UserAccount.objects.last()

    # if not ret.exists():
    #     return None

    return ret



def get_login_url() -> str:

    # TODO: Arahkan kepada login page yang sesungguhnya setelah Tito menyelesaikan login system-nya
    return "/admin"



