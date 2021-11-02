from django import forms

from models_app.models.UserAccount import UserAccount
from models_app.models.EntrepreneurAccount import EntrepreneurAccount
from models_app.models.InvestorAccount import InvestorAccount



class ProfileForm(forms.ModelForm) :
    class Meta:
        model = UserAccount
        fields = ("email", "username", "photo_profile", "full_name",
            "gender",
            "phone_number",
            "alamat",
            "deskripsi_diri",  
            # "enterpreneur_account",
            # "investor_account"
        )
    
    

