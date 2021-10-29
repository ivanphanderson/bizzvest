from io import BytesIO
from unittest import mock
from unittest.mock import Mock

from PIL import Image
from django.core.files.images import ImageFile
from django.test import Client, TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.core.files import File as django_file
from models_app.models import *
from halaman_toko.views import *
from halaman_toko.forms import *
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile

# Create your tests here.



def mock_image_field(nama="gambar asal asalan.jpg"):
    return SimpleUploadedFile(name=nama, content=open('test.jpg', 'rb').read(),
                              content_type='image/jpeg')
    # return mock.MagicMock(spec=django_file, name=nama)

    # image = Image.new('RGBA', size=(50,50), color=(256,0,0))
    # image_file = BytesIO()
    # image.save(image_file, 'PNG')  # or whatever format you prefer
    # return ImageFile(image_file)



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
        self.client = Client()
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="08128845191")
        temp_acc.photo_profile = mock_image_field()
        temp_acc.save()

        # TODO: login the temp_acc


    def test_add_toko(self):
        response = self.client.get('/halaman-toko/')
        self.assertNotEqual(response.status_code, 200)   # karena belum terdaftar

        response = self.client.get('/halaman-toko/edit-photo')
        self.assertNotEqual(response.status_code, 200)   # karena belum terdaftar

        response = self.client.get('/halaman-toko/add')
        self.assertEqual(response.status_code, 200)  # karena sudah login
        data = {
            'nama_merek': 'my merk',
            'nama_perusahaan': 'PT. my pt',
            'kode_saham': 'SDFG',
            'alamat': 'Jl. abcdef',
            'jumlah_lembar': '10000',
            'nilai_lembar_saham': '10000',
            'dividen': '12',
            'end_date': '2024-12-31',
            'deskripsi': 'my description',
            'is_validate_only': '1'
        }
        temp = CompanyAddForm(data=data)
        self.assertTrue(temp.is_valid())
        temp2 = UserAccount.objects.filter(username="shjkrk").first()
        self.assertIsNot(temp2, None)

        temp2.entrepreneuraccount = EntrepreneurAccount()
        temp2.entrepreneuraccount.save()

        temp.pemilik_usaha = temp2.entrepreneuraccount
        temp = temp.save()

        response = self.client.get('/halaman-toko/?id=' + str(temp.id))
        self.assertEqual(response.status_code, 200)  # karena sudah ada toko

        response = self.client.get('/halaman-toko/edit-photos?id=' + str(temp.id))
        self.assertEqual(response.status_code, 200)   # karena sudah terdaftar


class ManagePhotosTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="08128845191")
        temp_acc.photo_profile = mock_image_field()
        temp_acc.save()

        # TODO: login the temp_acc


    def test_responses(self):
        response = self.client.get('/halaman-toko/delete-photo')
        self.assertEqual(response.status_code, 400)   # karena cuman GET request

        response = self.client.get('/halaman-toko/photo-reorder')
        self.assertEqual(response.status_code, 400)   # karena cuman GET request

        response = self.client.get('/halaman-toko/upload-proposal')
        self.assertEqual(response.status_code, 400)   # karena cuman GET request

        response = self.client.get('/halaman-toko/request-for-verification')
        self.assertEqual(response.status_code, 400)   # karena cuman GET request

        response = self.client.post('/halaman-toko/add', {
            'pemilik_usaha':'1234'
        })
        self.assertEqual(response.status_code, 400)   # karena POSTnya ada atribut terlarang 'pemilik_usaha'




