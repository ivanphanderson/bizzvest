from django.urls import path
from .views import index, ganti_profil

urlpatterns = [
    path('', index, name='index'),
    path('ganti-profil', ganti_profil, name='ganti_profil'),
]
