from .UserAccount import *
from django.db import models





class InvestorAccount(models.Model):  # orang yang berinvestasi (pemberi pinjaman)
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Inv {self.account.user_model.username}>"



