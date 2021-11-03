from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.tampilkan_toko, name="tampilkan_toko"),
    path('experiment/', views.experiment, name='experiment'),
]
