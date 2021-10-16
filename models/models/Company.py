from .EntrepreneurAccountData import *
from django.utils import timezone
from django.db import models


class Company(models.Model):  # dengan nama lain: Toko
    pemilik_usaha = models.ForeignKey(EntrepreneurAccountData, on_delete=models.CASCADE)
    nama_merek = models.CharField(max_length=30)
    nama_perusahaan = models.CharField(max_length=35)
    deskripsi = models.TextField(max_length=3000, default="")


    # tidak terpengaruh oleh saham yg sudah dikumpulkan
    nilai_saham_dibutuhkan_total = models.BigIntegerField(blank=True, editable=False)

    nilai_saham_terkumpulkan_total = models.BigIntegerField(blank=True, editable=False)
    nilai_lembar_saham = models.BigIntegerField()  # nilai saham per lembar
    jumlah_lembar = models.BigIntegerField()  # jumlah lembar saham yang diperlukan

    dividen = models.IntegerField()  # dividen saham dalam satuan bulan
    start_date = models.DateField(default=timezone.now)  # waktu dan tanggal perusahaan ini mulai menerima saham
    end_date = models.DateField()  # waktu dan tanggal perusahaan ini sudah berhenti menerima saham

    def __str__(self):
        return f"<{self.nama_merek} -- {self.nama_perusahaan} -- {self.pemilik_usaha.account.username}>"

    def save(self, *args, **kwargs):
        self.nilai_saham_terkumpulkan_total = 0
        self.nilai_saham_dibutuhkan_total = self.nilai_lembar_saham * self.jumlah_lembar
        super().save(*args, **kwargs)


