from .UserAccount import *
from django.db import models





class InvestorAccountData(models.Model):  # orang yang berinvestasi (pemberi pinjaman)
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)




