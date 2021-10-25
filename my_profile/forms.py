from django import forms

from my_profile.models import Profil, Password

class ProfileForm(forms.ModelForm) :
    class Meta:
        model = Profil
        fields = '__all__'

class PasswordForm(forms.ModelForm) :
    class Meta:
        model = Password
        fields = '__all__'
