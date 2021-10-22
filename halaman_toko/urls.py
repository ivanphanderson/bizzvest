from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = 'halaman_toko'

urlpatterns = [
    url('^$', views.halaman_toko, name='halaman_toko'),
    path('edit-photos', views.manage_photos, name='edit_photos'),
    path('save-edited-company-form', views.save_company_form),
    path('add', views.add_toko),
    path('add-photo', views.add_photo),
    path('delete-photo', views.delete_photo),
]
