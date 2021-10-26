from django.db import models

# Create your models here.
class Profil(models.Model):
    full_name = models.CharField(max_length=30)
    email = models.BigIntegerField()
    phone = models.BigIntegerField()
    address = models.CharField(max_length=30)
    date_of_birth = models.DateField()

class Password(models.Model):
    current_password = models.CharField(max_length=30)
    new_password = models.CharField(max_length=30)
    confirm_new_password = models.CharField(max_length=30)