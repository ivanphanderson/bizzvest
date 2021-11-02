from django import forms

from models_app.models.UserAccount import UserAccount
from models_app.models.EntrepreneurAccount import EntrepreneurAccount
from models_app.models.InvestorAccount import InvestorAccount
from django.contrib.auth.models import User



class ProfileForm(forms.ModelForm) :
    class Meta:
        model = UserAccount
        fields = ("photo_profile", "full_name",
            "gender",
            "phone_number",
            "alamat",
            "deskripsi_diri",  
            # "enterpreneur_account",
            # "investor_account"
        )

class FormSpesial(forms.ModelForm) :
    class Meta:
        model = User
        fields = ("email", "username")
    
    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user    

