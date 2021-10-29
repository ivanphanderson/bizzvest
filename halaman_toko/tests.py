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


def mock_pdf_field(nama="pdf asal asalan.pdf"):
    return SimpleUploadedFile(name=nama, content=open('test.pdf', 'rb').read(),
                              content_type='application/pdf')




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
        temp2.is_entrepreneur = True


        temp.pemilik_usaha = temp2.entrepreneuraccount
        temp = temp.save()

        response = self.client.get('/halaman-toko/?id=' + str(temp.id))
        self.assertEqual(response.status_code, 200)  # karena sudah ada toko

        response = self.client.get('/halaman-toko/edit-photos?id=' + str(temp.id))
        self.assertEqual(response.status_code, 200)   # karena sudah terdaftar


class ManagePhotosTestNoLogin(TestCase):
    def setUp(self) -> None:
        pass

    def test_run(self):
        response = self.client.get('/halaman-toko/add-photo')
        self.assertEqual(response.status_code, 302)   # karena cuman GET request

class ManagePhotosTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="08128845191")
        temp_acc.photo_profile = mock_image_field()
        temp_acc.save()
        temp_acc.is_entrepreneur = True
        self.id = temp_acc

        # TODO: login the temp_acc
        self.comp = Company(pemilik_usaha=temp_acc.entrepreneuraccount, jumlah_lembar=10000, nilai_lembar_saham=12000,
                            deskripsi="Ini garam terlezat yang pernah ada", nama_merek="Garamku",
                            nama_perusahaan="PT. Sugar Sugar", alamat="Jl. Sirsak", kode_saham="ABCD",
                            dividen=12, status_verifikasi=Company.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI,
                            end_date=timezone.now())
        self.comp.proposal = mock_pdf_field()
        self.comp.full_clean()
        self.comp.save()
        self.comp_id = self.comp.id

        self.photo = CompanyPhoto(company=self.comp, img=mock_image_field(), img_index=1)
        self.photo.save()
        self.photo2 = CompanyPhoto(company=self.comp, img=mock_image_field(), img_index=2)
        self.photo2.save()


    def test_responses(self):
        response = self.client.get('/halaman-toko/delete-photo')
        self.assertEqual(response.status_code, 400)   # karena cuman GET request
        response = self.client.post('/halaman-toko/delete-photo')
        self.assertEqual(response.status_code, 400)   # karena cuman atribut tidak memadai

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


    def test_add_toko_add_photo(self):

        data = {
            'company_id': self.comp.id,
            'img': mock_image_field()
        }

        temp = data.copy();  temp.pop('company_id')
        response = self.client.post('/halaman-toko/add-photo', temp)
        self.assertEqual(response.status_code, 400)   # karena POSTnya ga ada atribut company_id

        temp = data.copy();  temp.pop('img')
        response = self.client.post('/halaman-toko/add-photo', temp)
        self.assertEqual(response.status_code, 400)   # karena POSTnya ga ada atribut img

        temp = data.copy();  temp['company-id'] = 'asd'
        response = self.client.post('/halaman-toko/add-photo', temp)
        self.assertEqual(response.status_code, 400)   # karena id invalid

        temp = data.copy();  self.comp.status_verifikasi = Company.StatusVerifikasi.MENGAJUKAN_VERIFIKASI;
        self.comp.save()
        response = self.client.post('/halaman-toko/add-photo', temp)
        self.assertEqual(response.status_code, 400)   # karena sudah sempat mengajukan verifikasi
        self.comp.status_verifikasi = Company.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI;
        self.comp.save()

        with open('test.jpg', 'rb') as fp:
            temp = data.copy()
            temp['img'] = fp
            response = self.client.post('/halaman-toko/add-photo', temp)
            self.assertEqual(response.status_code, 200)   # sudah valid




        # add toko
        response = self.client.get('/halaman-toko/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<input", response.content)


        response = self.client.post('/halaman-toko/add', {
            'pemilik_usaha':'1234'
        })
        self.assertEqual(response.status_code, 400)   # karena POSTnya ada atribut terlarang 'pemilik_usaha'

        data = {

        }


    def test_reorder(self):
        data = {
            'company_id': self.comp.id,
            'photo_order': json.dumps({
                str(self.photo.id): 3,
                str(self.photo2.id): 1
            })
        }

        temp = data.copy()
        response = self.client.post('/halaman-toko/photo-reorder', temp)
        self.assertEqual(response.status_code, 200)   # karena POSTnya ga ada atribut company_id


class HalamanPhotoTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="08128845191")
        temp_acc.photo_profile = mock_image_field()
        temp_acc.save()
        temp_acc.is_entrepreneur = True
        self.id = temp_acc

        # TODO: login the temp_acc
        self.comp = Company(pemilik_usaha=temp_acc.entrepreneuraccount, jumlah_lembar=10000, nilai_lembar_saham=12000,
                            deskripsi="Ini garam terlezat yang pernah ada", nama_merek="Garamku",
                            nama_perusahaan="PT. Sugar Sugar", alamat="Jl. Sirsak", kode_saham="ABCD",
                            dividen=12, status_verifikasi=Company.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI,
                            end_date=timezone.now())
        self.comp.proposal = mock_pdf_field()
        self.comp.full_clean()
        self.comp.save()
        self.comp_id = self.comp.id

        self.photo = CompanyPhoto(company=self.comp, img=mock_image_field(), img_index=1)
        self.photo.save()
        self.photo2 = CompanyPhoto(company=self.comp, img=mock_image_field(), img_index=2)
        self.photo2.save()

    def test_proposal(self):
        data = {
            'company_id': self.comp.id,
            'proposal': mock_pdf_field()
        }

        response = self.client.post('/halaman-toko/upload-proposal', data)
        self.assertEqual(response.status_code, 200)   # karena POSTnya ga ada atribut company_id
