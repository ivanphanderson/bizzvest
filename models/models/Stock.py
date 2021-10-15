from .InvestorAccountData import *
from .Company import *
from django.db import models





class Stock(models.Model):  # saham
    # pemegang saham
    holder = models.ForeignKey(InvestorAccountData, on_delete=models.CASCADE)

    # perusahaan tempat saham ini ditanamkan
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    nilai_saham = models.BigIntegerField()  # besarnya saham
    tanggal_ditanam = models.DateField(auto_now_add=True)
    tanggal_berakhir = models.DateField()


