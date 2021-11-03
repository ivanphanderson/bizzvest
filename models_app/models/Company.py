
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator

from halaman_toko.authentication_and_authorization import *
from models_app.validators import validate_pdf_file_extension
from .EntrepreneurAccount import *
from django.utils import timezone
from django.db import models





class Company(models.Model):  # dengan nama lain: Toko
    class StatusVerifikasi(models.IntegerChoices):
        BELUM_MENGAJUKAN_VERIFIKASI = 0
        MENGAJUKAN_VERIFIKASI = 1
        VERIFIKASI_DITOLAK = 2
        TERVERIFIKASI = 3

    pemilik_usaha = models.ForeignKey(EntrepreneurAccount, on_delete=models.CASCADE, blank=True, null=True)
    status_verifikasi = models.IntegerField(choices=StatusVerifikasi.choices, default=StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI)
    proposal = models.FileField(upload_to="uploads/proposals/%Y/%m/",
                                null=True,
                                blank=True,
                                validators=[validate_pdf_file_extension]
                                )

    nama_merek = models.CharField(max_length=30, unique=True, verbose_name='Nama merek')
    nama_perusahaan = models.CharField(max_length=35, verbose_name='Nama perusahaan')
    alamat = models.CharField(max_length=140, default="", verbose_name='Alamat')  # alamat toko
    deskripsi = models.TextField(max_length=3000, default="", verbose_name='Deskripsi')


    # jumlah lembar saham yang diperlukan
    jumlah_lembar = models.BigIntegerField(verbose_name='Jumlah lembar saham')

    # nilai saham per lembar
    nilai_lembar_saham = models.BigIntegerField(verbose_name='Nilai lembar saham')

    kode_saham = models.CharField(verbose_name="Kode saham",
                                  validators=[RegexValidator(regex='^[A-Z]{4}$', message='Must be upper case letters of 4 characters',
                                                             code='nomatch')],
                                  unique=True, max_length=4)

    # dividen saham dalam satuan bulan
    dividen = models.IntegerField(verbose_name='Dividen')

    # waktu dan tanggal perusahaan ini mulai menerima saham
    start_date = models.DateField(default=timezone.now, blank=True)

    # waktu dan tanggal perusahaan ini sudah berhenti menerima saham
    end_date = models.DateField(verbose_name='Batas waktu')

    def __str__(self):
        return f"<{self.nama_merek} -- {self.nama_perusahaan} -- {self.pemilik_usaha.account.user_model.username}>"

    def save(self, *args, **kwargs):
        if (self.pemilik_usaha is None):
            raise RuntimeError("Pemilik usaha none")

        super().save(*args, **kwargs)

    def get_first_image(self):
        return self.companyphoto_set.all().order_by("img_index")[0]


