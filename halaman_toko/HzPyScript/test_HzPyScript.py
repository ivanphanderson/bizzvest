from django.test import Client, TestCase
from django.urls import reverse


class HzPyScript(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_contoh1(self):
        response = self.client.get(reverse("halaman_toko:HzPyScript_contoh1"))
        self.assertEqual(response.status_code, 200)