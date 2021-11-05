from django.test import TestCase

# Create your tests here.

from io import BytesIO
from unittest import mock
from unittest.mock import Mock

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.test import Client, TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.core.files import File as django_file
from django.core.files.uploadedfile import SimpleUploadedFile
from models_app.models import *
from halaman_toko.forms.halaman_toko_add_form import CompanyAddForm
from .views import *




def mock_image_field(nama="gambar asal asalan.jpg"):
    return SimpleUploadedFile(name=nama, content=open('test.jpg', 'rb').read(),
                              content_type='image/jpeg')


def mock_pdf_field(nama="pdf asal asalan.pdf"):
    return SimpleUploadedFile(name=nama, content=open('test.pdf', 'rb').read(),
                              content_type='application/pdf')


def set_up(self):
    self.client = Client()

    PASSWORD = "ASDjighUEISghuiHE124246"
    USERNAME = "shjkrk"

    user_obj:User = User.objects.create()
    user_obj.set_password(PASSWORD)

    temp_acc = UserAccount(user_model=user_obj, full_name="sujhek kheruk",
                           deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                           phone_number="08128845191", saldo=200000)
    temp_acc.user_model.username=USERNAME
    temp_acc.user_model.email="shjkrk@localhost"

    temp_acc.photo_profile = mock_image_field()
    temp_acc.save()  # automatically save the user_obj
    self.temp_acc = temp_acc

    login = self.client.login(username=USERNAME, password=PASSWORD)
    self.assertTrue(login)
    return temp_acc


class MulaiInvestTest(TestCase):
    def test_mulai_invest_response(self):
        response = Client().get('/mulai-invest/')
        self.assertNotEqual(response.status_code, 200)

    def test_manage_toko_response(self):
        response = Client().get('/mulai-invest/status-invest')
        self.assertNotEqual(response.status_code, 200)

class MulaiInvestLoginTest(TestCase):
    def setUp(self) -> None:
        set_up(self)


    def test_mulai_invest(self):
    
        data = {
            'nama_merek': 'my merk',
            'nama_perusahaan': 'PT. my pt',
            'kode_saham': 'SDFG',
            'alamat': 'Jl. abcdef',
            'jumlah_lembar': '10000',
            'nilai_lembar_saham': '10000',
            'dividen': '12',
            'end_date': '2024-12-31',
            'deskripsi': 'my sdescription',
            'is_validate_only': '1'
        }

        temp_form = CompanyAddForm(data=data)
        self.assertTrue(temp_form.is_valid())
        temp2 = UserAccount.objects.filter(user_model__username="shjkrk").first()
        self.assertIsNot(temp2, None)
        temp2.is_entrepreneur = True


        temp = temp_form.save(commit=False)
        temp.pemilik_usaha = temp2.entrepreneuraccount
        temp.save()


        response = self.client.get('/mulai-invest/?id=' + str(temp.id))
        self.assertEqual(response.status_code, 200)  # karena sudah ada toko

        response = self.client.get('/mulai-invest/status-invest')
        self.assertEqual(response.status_code, 200)   # karena sudah terdaftar
