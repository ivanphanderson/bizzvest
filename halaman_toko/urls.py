from django.urls import path
from . import views

app_name = 'home_page'

urlpatterns = [
    path('', views.halaman_toko, name='halaman_toko'),
    path('/edit-photos', views.edit_photos, name='edit_photos'),
    path('/save-edited-company-form', views.save_company_form),
    path('/add', views.add_toko),
]
