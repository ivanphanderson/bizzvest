from django.urls import path
from . import views

app_name = 'home_page'

urlpatterns = [
    path('', views.halaman_toko, name='halaman_toko'),
]
