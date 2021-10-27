from django.db import models

# Create your models here.
class Faq(models.Model):
    #TODO: membuat default dari nama menjadi nama kalo login, kalo tidak login harusnya form ga muncul
    nama = models.CharField(max_length=30, default= "anonymous")
    pertanyaan = models.TextField()
