from django.db import models

# Create your models here.
class Faq(models.Model):
    nama = models.CharField(max_length=30)
    pertanyaan = models.TextField()
