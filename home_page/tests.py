from django.test import TestCase
from django.test import Client
from django.urls import resolve
from .views import index, add_message
from .models import Message

# Create your tests here.
class HomepageTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_home_page_is_exist(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_using_index_func(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_message_attributes(self):
        obj1 = Message.objects.create(email="ghozi@bizzvest.com", message='Site ini sangat bagus, saya suka!')
        self.assertEqual(obj1.email, 'ghozi@bizzvest.com')
        self.assertEqual(obj1.message, 'Site ini sangat bagus, saya suka!')

    def test_json(self):
        Message.objects.create(email="ghozi@bizzvest.com", message='Site ini sangat bagus, saya suka!')
        response = self.client.post('/', {'email': 'ghozi@bizzvest.com', 'message': 'Site ini sangat bagus, saya suka!'})
        self.assertEqual(response.status_code, 200)

    def test_add_message(self):
        response = self.client.post('/save-message/')
        self.assertEqual(response.status_code, 200)

    def test_valid_message(self):
        dictio = {"email": "email@domain.com", "message": "Ini uji coba mengirim pesan"}
        response = self.client.post('/save-message/', dictio)
        self.assertEqual(response.status_code, 200)
