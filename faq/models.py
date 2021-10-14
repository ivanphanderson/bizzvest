from django.db import models

# Create your models here.
class Faq(models.Model):
    pertanyaan = models.TextField()
    jawaban = models.TextField()