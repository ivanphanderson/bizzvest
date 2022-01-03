import warnings

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models
from random import choices
import string



def random_password():
    temp1 = choices(string.ascii_uppercase)
    temp2 = choices(string.ascii_lowercase)
    temp3 = choices(string.digits)
    return f"{temp1}{temp2}{temp3}"

gender_choices = (
    ('jenis_kelamin', 'Pilih jenis kelamin'),
    ('laki_laki', 'Laki-laki'),
    ('perempuan', 'Perempuan'),
)

class UserAccount(models.Model):
    FORWARD_ATTR = {'username', 'email'}

    def __init__(self, *args, **kwargs):

        keys = ('username', 'email')
        key_result = {}
        for key in keys:
            if key in kwargs:
                key_result[key] = kwargs.pop(key)

        if 'user_model' in kwargs and kwargs['user_model'] is User:
            warnings.warn('user_model is not specified with User() object. A new user object with '
                          'random password will be created')
            temp = User(password=random_password(), **key_result)
            kwargs['user_model'] = temp
            temp.save()

        super().__init__(*args, **kwargs)

    USERNAME_VALIDATORS = [RegexValidator(regex='^[a-zA-Z0-9_]{4,14}$',
                                          message='Must consists only lowercase alphanumeric characters '
                                                  'and underscore. The length should be 4 to 14 characters',
                                          code='nomatch')]

    user_model = models.OneToOneField(User, on_delete=models.CASCADE)

    # username = models.CharField(max_length=14, unique=True, db_index=True, null=True,
    #                             validators=USERNAME_VALIDATORS)
    # email = models.EmailField(max_length=254, unique=True, null=True, db_index=True)



    # @property
    # def username(self):
    #     return self.user_model.username
    #
    # @username.setter
    # def username(self, value):
    #     print('setting')
    #     self.user_model.username = value
    #
    # @property
    # def email(self):
    #     return self.user_model.email
    #
    # @email.setter
    # def email(self, value):
    #     self.user_model.email = value



    photo_profile = models.ImageField(upload_to="uploads/user_profile/%Y/%m/", default="default_user_photoprofile.jpg", blank=True)
    phone_number = models.CharField(default="0000000000", blank=True, max_length=15,
                                    validators=[
                                        RegexValidator(regex='^0[0-9]{8,14}$',
                                                       message='Must consists only digits started by zero, then'
                                                               'followed by 8 to 14 digits',
                                                       code='nomatch')])

    full_name = models.CharField(max_length=23, default="", blank=True,
                                 validators=[
                                     # RegexValidator(regex='^[a-zA-Z]?[a-z]*( [a-zA-Z][a-z]*)*$',
                                     RegexValidator(regex='^[a-zA-Z ]+$',
                                                    message='Must consists only alphabets. Only first letters in each '
                                                            'word are allowed to be uppercase. No two consecutive '
                                                            'spaces are allowed',
                                                    code='nomatch')])

    alamat = models.CharField(max_length=140, default="", blank=True)
    deskripsi_diri = models.TextField(max_length=3000, default="", blank=True)
    gender = models.CharField(max_length=20, choices=gender_choices, default='jenis-kelamin', blank=True)
    saldo = models.BigIntegerField(default=0)
    ### sepertinya tidak perlu
    # join_date = models.DateField(default=timezone.now)
    # last_login = models.DateTimeField(default=timezone.now)

    @property
    def is_investor(self):
        return hasattr(self, 'investoraccount') and self.investoraccount is not None 

    @is_investor.setter
    def is_investor(self, value):
        from models_app.models import InvestorAccount
        if (self.is_investor is not value and self.is_investor != value):  # then update
            if value:
                self.investoraccount = InvestorAccount(account=self)
                self.investoraccount.save()

            else:
                self.investoraccount.delete()
                self.investoraccount = None
               


    @property
    def is_entrepreneur(self):
        return hasattr(self, 'entrepreneuraccount')

    @is_entrepreneur.setter
    def is_entrepreneur(self, value):
        from models_app.models import EntrepreneurAccount
        if (self.is_entrepreneur is not value and self.is_entrepreneur != value):  # then update
            if value:
                self.entrepreneuraccount = EntrepreneurAccount(account=self)
                self.entrepreneuraccount.save()
                
            else:
                self.entrepreneuraccount.delete()
                self.entrepreneuraccount = None
                


    def __str__(self):
        return f"<{self.user_model.username} {self.user_model.email}>"

    def save(self, *args, **kwargs):
        self.user_model.save()
        super().save(*args, **kwargs)

    # def __getattribute__(self, item):
    #     sself = self
    #
    #     class custom_objects():
    #         def filter(self, *args, **kwargs):
    #             if len(set(kwargs.keys()) & UserAccount.FORWARD_ATTR) != 0:
    #                 return sself.user_model.objects.filter(*args, **kwargs)
    #             return sself.objects.filter(*args, **kwargs)
    #
    #         def __getattribute__(self, item):
    #             if item != 'filter':
    #                 return getattr(sself.objects, item)
    #             return self.filter
    #
    #     if item in UserAccount.FORWARD_ATTR:
    #         return custom_objects()
    #     return super().__getattribute__(item)
    #
    # def __setattr__(self, key, value):
    #     if key in UserAccount.FORWARD_ATTR:
    #         return self.user_model.__setattr__(key, value)
    #     return super().__setattr__(key, value)

