"""BizzVest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    re_path('admin/?', admin.site.urls),
    path('', include('home_page.urls')),
    path('faq/', include('faq.urls')),
    path('start-web/', include('start_web.urls')),
    path('mulai-invest/', include('mulai_invest.urls')),
    path('daftar-toko/', include('daftar_toko.urls')),
    path('daftar-toko', RedirectView.as_view(url='daftar-toko/', permanent=False)),

    path('halaman-toko/', include('halaman_toko.urls')),
    path('halaman-toko', RedirectView.as_view(url='halaman-toko/', permanent=False)),
    path('add-toko', RedirectView.as_view(url='halaman-toko/add', permanent=False)),

    path('my-profile/', include('my_profile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
