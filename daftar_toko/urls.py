from django.urls import path
from . import views


urlpatterns = [
    path('', views.tampilkan_toko, name="tampilkan_toko"),
    path('search/', views.search, name="search"),
]
