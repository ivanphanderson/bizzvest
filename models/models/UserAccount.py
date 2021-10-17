from django.utils import timezone
from django.db import models





class UserAccount(models.Model):
    username = models.CharField(max_length=24, unique=True, db_index=True, null=True)
    email = models.EmailField(max_length=254, unique=True, null=True)

    photo_profile = models.ImageField(upload_to="uploads/user_profile/%Y/%m/", null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    join_date = models.DateField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"<{self.username} {self.email}>"



