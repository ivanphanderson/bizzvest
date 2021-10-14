from django.urls import path
from . import views

app_name = 'home_page'

urlpatterns = [
    path('', views.index, name='home_page_index'),
]
