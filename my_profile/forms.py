from django import forms

from models_app.models.UserAccount import UserAccount

class ProfileForm(forms.ModelForm) :
    class Meta:
        model = UserAccount
        fields = {"email", "username", "photo_profile", "full_name",  "is_verified", "join_date",
    "last_login",
    "jenis_kelamin",
    "phone",
    "address",
    "description", 
    "password_user"}
    
    

