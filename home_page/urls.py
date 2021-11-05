from django.urls import path
from .views import index, add_message

app_name = 'home_page'

urlpatterns = [
    path('', index, name='index'),
    path('save-message/', add_message, name='save_message'),
]
