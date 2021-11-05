from typing import Reversible
from django.test import TestCase
from django.test import Client
from django.urls import resolve
from .views import *

# Create your tests here.
class daftarTokoTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_daftar_toko_is_exist(self):
        response = Client().get('/daftar-toko/')
        self.assertEqual(response.status_code, 200)

    def test_using_index_func(self):
        found = resolve('/daftar-toko/')
        self.assertEqual(found.func, tampilkan_toko)

    