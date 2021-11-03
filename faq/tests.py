from django.test import TestCase
from django.test import Client
from django.urls import resolve
from .views import *


class FAQTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_faq_is_exist(self):
        response = Client().get('/faq/')
        self.assertEqual(response.status_code, 200)

    def test_using_index_func(self):
        found = resolve('/faq/')
        self.assertEqual(found.func, index)

    def test_faq_attributes(self):
        obj1 = Faq.objects.create(nama='Nandhita Zefana Maharani', pertanyaan='Apakah keuntungan dari mengikuti BizzVest?')
        self.assertEqual(obj1.nama, 'Nandhita Zefana Maharani')
        self.assertEqual(obj1.pertanyaan, 'Apakah keuntungan dari mengikuti BizzVest?')

    def test_json(self):
        Faq.objects.create(nama='Nandhita Zefana Maharani', pertanyaan='Apakah keuntungan dari mengikuti BizzVest?')
        response = self.client.post('/faq/', {'nama': 'Nandhita Zefania Maharani', 'pertanyaan': 'Apakah keuntungan dari mengikuti BizzVest?'})
        self.assertEqual(response.status_code, 200)

    def test_post_faq(self):
        response = self.client.post('/faq/save/')
        self.assertEqual(response.status_code, 200)

    def test_valid_faq(self):
        dictio = {"nama": "Nandhita Zefania Maharani", "pertanyaan": "Ini uji coba"}
        response = self.client.post('/faq/save/', dictio)
        self.assertEqual(response.status_code, 200)





