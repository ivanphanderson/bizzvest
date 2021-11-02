from itertools import permutations

from django.test import Client, TestCase
from models_app.models import *
from halaman_toko.views import *
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile

# Create your tests here.


def mock_image_field(nama="gambar asal asalan.jpg"):
    return SimpleUploadedFile(name=nama, content=open('test.jpg', 'rb').read(),
                              content_type='image/jpeg')


def mock_pdf_field(nama="pdf asal asalan.pdf"):
    return SimpleUploadedFile(name=nama, content=open('test.pdf', 'rb').read(),
                              content_type='application/pdf')


class Company_and_CompanyAccount_test(TestCase):
    def test_run(self) -> None:
        temp_acc = UserAccount(full_name="sujhek kheruk", user_model=User,
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="08128845191")
        temp_acc.user_model.username="shjkrk"
        temp_acc.user_model.email="shjkrk@localhost"
        temp_acc.photo_profile = mock_image_field()
        temp_acc.save()
        temp_acc.is_entrepreneur = True
        self.id = temp_acc.id

        temp_comp = Company()
        temp_comp.pemilik_usaha = temp_acc.entrepreneuraccount
        temp_comp.status_verifikasi = Company.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI
        temp_comp.proposal = mock_pdf_field()
        temp_comp.jumlah_lembar = 10000
        temp_comp.nilai_lembar_saham = 12000
        temp_comp.deskripsi = "Ini garam terlezat yang pernah ada"
        temp_comp.nama_merek = "Garamku"
        temp_comp.nama_perusahaan = "PT. Sugar Sugar"
        temp_comp.alamat = "Jl. Sirsak"
        temp_comp.dividen = 12
        temp_comp.kode_saham = "ABCD"
        temp_comp.end_date = timezone.now()
        temp_comp.full_clean()
        temp_comp.save()
        self.comp_id = temp_comp.id
