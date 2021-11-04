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


def set_up(self):
    self.client = Client()

    PASSWORD = "ASDjighUEISghuiHE124246"
    USERNAME = "shjkrk"

    user_obj:User = User.objects.create()
    user_obj.set_password(PASSWORD)

    temp_acc = UserAccount(user_model=user_obj, full_name="sujhek kheruk",
                           deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                           phone_number="08128845191")
    temp_acc.user_model.username=USERNAME
    temp_acc.user_model.email="shjkrk@localhost"

    temp_acc.photo_profile = mock_image_field()
    temp_acc.save()  # automatically save the user_obj
    self.temp_acc = temp_acc

    login = self.client.login(username=USERNAME, password=PASSWORD)
    self.assertTrue(login)
    return temp_acc



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
        set_up(self)


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
        temp_form = CompanyAddForm(data=data)
        self.assertTrue(temp_form.is_valid())
        temp2 = UserAccount.objects.filter(user_model__username="shjkrk").first()
        self.assertIsNot(temp2, None)
        temp2.is_entrepreneur = True


        temp = temp_form.save(commit=False)
        temp.pemilik_usaha = temp2.entrepreneuraccount
        temp.save()


        response = self.client.get('/halaman-toko/?id=' + str(temp.id))
        self.assertEqual(response.status_code, 200)  # karena sudah ada toko

        response = self.client.get('/halaman-toko/edit-photos?id=' + str(temp.id))
        self.assertEqual(response.status_code, 200)   # karena sudah terdaftar



class HalamanTokoLagi(TestCase):
    def setUp(self) -> None:
        temp_acc = set_up(self)
        temp_acc.is_entrepreneur = True
        self.id = temp_acc

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
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/halaman-toko/upload-proposal', {
            'company_id': self.comp.id,
            'proposal': mock_pdf_field(nama="asdfg.jpg")
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/halaman-toko/upload-proposal', {
            'proposal': mock_pdf_field()
        })
        self.assertEqual(response.status_code, 400)  # field doesn't exist: company_id

        response = self.client.post('/halaman-toko/upload-proposal', {
            'company_id': 9999999999999,
            'proposal': mock_pdf_field()
        })
        self.assertEqual(response.status_code, 400)  # error  company_id not found


    def test_edit_deskripsi(self):
        totally_random_string = 'kjoigjsiogjior iowjtgoiwjytoi jhiorjeyh94jyu895hy'
        response = self.client.post('/halaman-toko/save-edited-company-form', {
            'id': self.comp.id,
            'deskripsi': totally_random_string
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/halaman-toko/save-edited-company-form', {
            'id': self.comp.id,
            'deskripsi': ''
        })
        self.assertEqual(response.status_code, 400)   # karena isinya kosong

        response = self.client.get('/halaman-toko/?id=' + str(self.comp_id))
        self.assertIn(totally_random_string.encode('utf-8'), response.content)


    def test_ajukan_verifikasi(self):
        # tidak perlu upload proposal maupun foto krn sudah diinisiasikan di setUp()
        data = {
                'id': self.comp.id
        }
        response = self.client.post('/halaman-toko/request-for-verification', data)
        self.assertEqual(response.status_code, 200)   # karena POSTnya ga ada atribut company_id



class ManagePhotosTestNoLogin(TestCase):
    def setUp(self) -> None:
        pass

    def test_run(self):
        response = self.client.get('/halaman-toko/add-photo')
        self.assertEqual(response.status_code, 302)   # karena cuman GET request


class ManagePhotosTest(TestCase):
    def setUp(self) -> None:
        temp_acc = set_up(self)
        temp_acc.is_entrepreneur = True
        self.acc = temp_acc
        self.id = temp_acc

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

        temp = data.copy();  temp['company_id'] = 3296349
        response = self.client.post('/halaman-toko/add-photo', temp)
        self.assertEqual(response.status_code, 400)   # karena company_id nya invalid

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

        for i in range(12):
            with open('test.jpg', 'rb') as fp:
                temp = data.copy()
                temp['img'] = fp
                response = self.client.post('/halaman-toko/add-photo', temp)
        with open('test.jpg', 'rb') as fp:
            temp = data.copy()
            temp['img'] = fp
            response = self.client.post('/halaman-toko/add-photo', temp)
            self.assertEqual(response.status_code, 400)   # karena tidak boleh menambahkan lebih dari 12 foto
        self.assertEqual(self.client.get('/halaman-toko/add-photo').status_code, 400)  # must be a post request

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

        data = {
            'company_id': self.comp.id,
            'photo_order': json.dumps({
                str(self.photo.id): 100000000,
                str(self.photo2.id): 1
            })
        }

        temp = data.copy()
        response = self.client.post('/halaman-toko/photo-reorder', temp)
        self.assertEqual(response.status_code, 400)   # invalid value photo id

        data = {
            'company_id': self.comp.id,
            'photo_order': json.dumps({
                str(self.photo.id): 100000000,
                str(self.photo2.id): 1
            })[1:]
        }

        temp = data.copy()
        response = self.client.post('/halaman-toko/photo-reorder', temp)
        self.assertEqual(response.status_code, 400)   # invalid json


    def test_delete_photos(self):
        new_photo = CompanyPhoto()
        new_photo.company = self.comp
        new_photo.img_index = self.comp.companyphoto_set.all().count() + 1  # + 1 karena one-based index
        new_photo.img = mock_image_field()
        new_photo.save()

        response = self.client.post('/halaman-toko/delete-photo', {
            'photo_id': new_photo.id
        })
        self.assertEqual(response.status_code, 200)   # karena POSTnya ga ada atribut company_id

class AddTokoTest(TestCase):
    def setUp(self) -> None:
        temp_acc = set_up(self)
        temp_acc.is_entrepreneur = True
        self.id = temp_acc
        self.acc = temp_acc

    def test_add_toko(self):
        string_acak = "HUIHgU rgnoiR rneo srg IH"
        assert len(string_acak) < 28, len(string_acak)

        data = {
            'nama_merek': string_acak,
            'nama_perusahaan': 'nama_perusahaan',
            'kode_saham': 'KODE',
            'alamat': 'Jl. sirsak pepaya',
            'jumlah_lembar': 12000,
            'nilai_lembar_saham': 20000,
            'dividen': 18,
            'end_date': '9999-02-02',
            'deskripsi': 'ini deskripsi',
            'is_validate_only': 1
        }

        response = self.client.post('/halaman-toko/add', data)
        # print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Company.objects.filter(nama_merek=string_acak).count(), 0)

        data = {
            'nama_merek':  string_acak,
            'nama_perusahaan': 'nama_perusahaan',
            'kode_saham': 'KODE',
            'alamat': 'Jl. sirsak pepaya',
            'jumlah_lembar': 12000,
            'nilai_lembar_saham': 20000,
            'dividen': 18,
            'end_date': '9999-02-02',
            'deskripsi': 'ini deskripsi',
            'is_validate_only': 0
        }

        self.acc.is_entrepreneur = False
        response = self.client.post('/halaman-toko/add', data)
        self.assertTrue(response.status_code in (200, 302))
        self.assertGreater(Company.objects.all().filter(nama_merek=string_acak).count(), 0)

    def test_add_toko_2(self):
        # add toko
        response = self.client.get('/halaman-toko/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<input", response.content)

        response = self.client.post('/halaman-toko/add', {
            'pemilik_usaha':'1234'
        })
        self.assertEqual(response.status_code, 400)   # karena POSTnya ada atribut terlarang 'pemilik_usaha'



class Utility(TestCase):
    def test_validate_toko_id(self):
        validate_toko_id("asdfgh")
