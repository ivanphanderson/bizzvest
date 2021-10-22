from .InvestorAccount import *
from .Company import *
from django.db import models





class Stock(models.Model):  # saham
    # pemegang saham
    holder = models.ForeignKey(InvestorAccount, on_delete=models.CASCADE)

    # perusahaan tempat saham ini ditanamkan
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    jumlah_lembar_saham = models.BigIntegerField()  # banyaknya lembar saham yang dibeli
    tanggal_ditanam = models.DateField(auto_now_add=True)
    tanggal_berakhir = models.DateField()

    def __str__(self):
        return f"<Stock at {self.company.nama_merek} -- {self.jumlah_lembar_saham} @ {self.company.nilai_lembar_saham}>"
