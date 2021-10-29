from django.test import Client, TestCase
from django.urls import resolve
from django.http import HttpRequest
from models_app import models

# Create your tests here.



class HalamanTokoTest(TestCase):
    def test_halaman_toko_response(self):
        response = Client().get('/halaman-toko/')
        self.assertNotEqual(response.status_code, 200)

    def test_manage_toko_response(self):
        response = Client().get('/halaman-toko/edit-photos')
        self.assertNotEqual(response.status_code, 200)

    def test_add_toko(self):
        response = Client().get('/halaman-toko/add')
        self.assertEqual(response.status_code, 302)  # karena belum login, diarahkan ke halaman login


class HalamanTokoSudahLoginTest(TestCase):
    def setUp(self) -> None:
        UserAccount.objects.create()

    def test_halaman_toko_response(self):
        response = Client().get('/halaman-toko/')
        self.assertNotEqual(response.status_code, 200)

    def test_manage_toko_response(self):
        response = Client().get('/halaman-toko/edit-photos')
        self.assertNotEqual(response.status_code, 200)

    def test_add_toko(self):
        response = Client().get('/halaman-toko/add')
        self.assertEqual(response.status_code, 302)  # karena belum login, diarahkan ke halaman login

