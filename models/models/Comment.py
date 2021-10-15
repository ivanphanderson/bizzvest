from .Company import *
from .UserAccount import *
from django.db import models





class Comment(models.Model):  # komentar yang telah di posting pada halaman toko
    id = models.AutoField(primary_key=True)
    commenter = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    post_target = models.ForeignKey(Company, on_delete=models.CASCADE)
    post_time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)



