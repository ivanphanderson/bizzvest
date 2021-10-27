from django.urls import path
from .views import ganti_password, index, ganti_profil

urlpatterns = [
    path('', index, name='index'),
    path('ganti-profil', ganti_profil, name='ganti_profil'),
    path('ganti_password', ganti_password, name='ganti_password')
]
