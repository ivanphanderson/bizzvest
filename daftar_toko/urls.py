from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.tampilkan_toko, name="tampilkan_toko"),
    url(r'^search/$', views.search, name='search'),
]
