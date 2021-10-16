from .Company import *
from django.utils import timezone
from django.db import models


class CompanyPhoto(models.Model):  # dengan nama lain: Toko
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    img = models.ImageField()
    img_index = models.IntegerField()

    def __str__(self):
        return f"<{self.company.nama_merek} -- {self.img}>"



