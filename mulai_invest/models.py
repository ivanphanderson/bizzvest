from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from models_app.models import UserAccount


# Create your models here.
# Probably not used
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     saldo = models.BigIntegerField(default=0)

#     def __str__(self):
#         return self.user.username




