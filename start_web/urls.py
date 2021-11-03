from django.urls import path
from . import views


urlpatterns = [
    path('login', views.log_in, name='login'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('logout', views.log_out, name='logout')
]
