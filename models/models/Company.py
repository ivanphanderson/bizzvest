from .EntrepreneurAccountData import *
from django.utils import timezone
from django.db import models


class Company(models.Model):  # dengan nama lain: Toko
    pemilik_usaha = models.ForeignKey(EntrepreneurAccountData, on_delete=models.CASCADE)
    nama_merek = models.CharField(max_length=30)
    nama_perusahaan = models.CharField(max_length=35)

    nilai_saham_dibutuhkan_total = models.BigIntegerField()
    nilai_saham_terkumpulkan_total = models.BigIntegerField()

    nilai_saham = models.BigIntegerField()  # nilai saham per lembar
    jumlah_lembar = models.BigIntegerField()  # jumlah lembar saham yang diperlukan

    dividen = models.IntegerField()  # dividen saham dalam satuan bulan
    start_date = models.DateTimeField(default=timezone.now)  # waktu dan tanggal perusahaan ini mulai menerima saham
    end_date = models.DateTimeField()  # waktu dan tanggal perusahaan ini sudah berhenti menerima saham




