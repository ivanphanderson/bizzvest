from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models





class UserAccount(models.Model):
    username = models.CharField(max_length=24, unique=True, db_index=True, null=True,
                                validators=[
                                    RegexValidator(regex='^[a-z0-9_]+$',
                                                   message='Must consists only lowercase alphanumeric and underscore '
                                                           'characters',
                                                   code='nomatch')])
    email = models.EmailField(max_length=254, unique=True, null=True)

    photo_profile = models.ImageField(upload_to="uploads/user_profile/%Y/%m/", null=True)
    full_name = models.CharField(max_length=12)
    is_verified = models.BooleanField(default=False)
    # foto_ktp = models.ImageField(upload_to="uploads/foto_ktp/%Y/%m/", null=True)
    # selfie_ktp = models.ImageField(upload_to="uploads/selfie_ktp/%Y/%m/", null=True)
    join_date = models.DateField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    jenis_kelamin = models.CharField(max_length=14)
    phone = models.BigIntegerField(max_length=12)
    address = models.CharField(max_length=30)
    description = models.TextField()
    password_user = models.CharField(max_length=25)


    def __str__(self):
        return f"<{self.username} {self.email}>"



