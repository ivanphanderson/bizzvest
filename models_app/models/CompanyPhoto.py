from django.core.exceptions import ValidationError

from .Company import *
from django.utils import timezone
from django.db import models

# def validate_image(fieldfile_obj):
#     filesize = fieldfile_obj.file.size
#     KB_limit = 150
#     if filesize > KB_limit * 1024:
#         raise ValidationError(f"Max file size is {KB_limit} KB")


print(models)
print(models.ImageField)
class CompanyPhoto(models.Model):  # dengan nama lain: Toko

    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # img = models.ImageField(upload_to="uploads/company_photos/%Y/%m/", validators=[validate_image])
    img = models.ImageField(upload_to="uploads/company_photos/%Y/%m/")

    img_index = models.IntegerField()
    alt = models.CharField(max_length=50, default="", blank=True)
    caption = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return f"<{self.company.nama_merek} -- {self.img}>"



