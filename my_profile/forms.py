from django import forms

from models_app.models.UserAccount import UserAccount
from models_app.models.EntrepreneurAccount import EntrepreneurAccount
from models_app.models.InvestorAccount import InvestorAccount



class ProfileForm(forms.ModelForm) :
    class Meta:
        model = UserAccount, EntrepreneurAccount, InvestorAccount
        fields = {"email", "username", "photo_profile", "full_name",
    "last_login",
    "jenis_kelamin",
    "phone",
    "alamat",
    "deskripsi_diri", 
    "password_user", 
    "i"}
    
    

