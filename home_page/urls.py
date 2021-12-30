from django.urls import path
from .views import index, add_message, json_message, save_api

app_name = 'home_page'

urlpatterns = [
    path('', index, name='index'),
    path('save-message/', add_message, name='save_message'),
    path('json', json_message),
    path('save-api/', save_api)
]
