from .Company import *
from django.utils import timezone
from django.db import models


class CompanyPhoto(models.Model):  # dengan nama lain: Toko
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="uploads/company_photos/%Y/%m/")
    img_index = models.IntegerField()
    alt = models.CharField(max_length=50, default="", blank=True)
    caption = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return f"<{self.company.nama_merek} -- {self.img}>"



