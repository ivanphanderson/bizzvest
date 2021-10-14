from django.db import models





class UserAccount(models.Model):
    user_id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)




