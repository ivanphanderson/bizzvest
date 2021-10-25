from django.conf.urls import url
from django.urls import path, re_path

import halaman_toko.views.halaman_toko
from . import views

app_name = 'halaman_toko'

urlpatterns = [
    url('^$', views.halaman_toko, name='halaman_toko'),
    path('edit-photos', views.manage_photos, name='edit_photos'),
    path('save-edited-company-form', views.save_company_form),
    path('add', views.add_toko),
    path('add-photo', views.add_photo),
    path('delete-photo', views.delete_photo),
    path('photo-reorder', views.photo_reorder),
    path('upload-proposal', views.edit_proposal, name="upload_proposal"),
    path('request-for-verification', views.ajukan_verifikasi, name="ajukan_verifikasi"),
]
