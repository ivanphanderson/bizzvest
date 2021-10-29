from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models


class UserAccount(models.Model):
    username = models.CharField(max_length=14, unique=True, db_index=True, null=True,
                                validators=[
                                    RegexValidator(regex='^[a-z0-9_]+$',
                                                   message='Must consists only lowercase alphanumeric and underscore '
                                                           'characters',
                                                   code='nomatch')])
    email = models.EmailField(max_length=254, unique=True, null=True, db_index=True)

    photo_profile = models.ImageField(upload_to="uploads/user_profile/%Y/%m/", null=True)
    phone_number = models.CharField(null=False, blank=False, unique=True, max_length=15,
                                    validators=[
                                        RegexValidator(regex='^0[0-9]{8,14}$',
                                                       message='Must consists only digits started by zero, then'
                                                               'followed by 8 to 14 digits',
                                                       code='nomatch')])

    full_name = models.CharField(max_length=30,
                                 validators=[
                                     RegexValidator(regex='^[a-zA-Z][a-z]*( [a-zA-Z][a-z]*)*$',
                                                    message='Must consists only alphabets. Only first letters in each '
                                                            'word are allowed to be uppercase. No two consecutive '
                                                            'spaces are allowed',
                                                    code='nomatch')])

    alamat = models.CharField(max_length=140, default="")
    deskripsi_diri = models.TextField(max_length=3000, default="")

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
        return f"<{self.username} {self.email}>"



