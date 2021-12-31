from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url('^$', views.mulai_invest, name='mulai_invest'),
    url('status-invest', views.status_investasi, name='status_invest'),
    path('ajax/update-saldo',  views.update_saldo_ajax, name='update_saldo'),
    path('ajax/beli-saham',  views.beli_saham, name='beli_saham'),
    path('flutter/get-saldo', views.get_saldo, name='get_saldo'),
    path('invest', views.get_invest_stuff, name='invest'),
    path('flutter/update-saldo', views.update_saldo_flutter, name='update_saldo_flutter'),
    path('flutter/beli-saham', views.beli_saham_flutter, name='beli_saham_flutter'),
]
