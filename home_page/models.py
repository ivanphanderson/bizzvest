from django.db import models
 
# Create your models here.
class Message(models.Model):
    email = models.CharField(max_length=30)
    message = models.TextField()
