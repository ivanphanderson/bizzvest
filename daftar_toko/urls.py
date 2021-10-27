from django.urls import path
from . import views


urlpatterns = [
    path('', views.tampilkan_toko, name="daftar_toko"),
]
