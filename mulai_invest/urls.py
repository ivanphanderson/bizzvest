from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    # path('register/', views.registerPage, name="register"),
	# path('login/', views.loginPage, name="logins"),  
	# path('logout/', views.logoutUser, name="logouts"),
    url('^$', views.halaman_toko, name='halaman_toko'),
    path('ajax/update-saldo',  views.UpdateSaldo.as_view(), name='update_saldo'),
    path('ajax/beli-saham',  views.BeliSaham.as_view(), name='beli_saham')
]
