from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('login', views.log_in, name='login'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('logout', views.log_out, name='logout'),
    path('validate-username', csrf_exempt(views.UsernameValidation.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(views.EmailValidation.as_view()), name='validate-email')
]
