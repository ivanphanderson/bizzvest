from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from models_app.models import Stock
# from .models import Profile

# class SaldoForm(forms.ModelForm):
#     class Meta:  
#         model = UserAccount
#         fields = '__all__'

        # error_messages = {'DOB' : {'invalid': "Mohon mengisi DOB dengan format yyyy-mm-dd"}}

# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['saldo']


# class ExtendedUserForm(UserCreationForm):
#     email=forms.EmailField(required=True)
#     first_name=forms.CharField(max_length=30)
#     last_name=forms.CharField(max_length=150)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

#     def save(self, commit=True):
#         user=super().save(commit=False)

#         user.email=self.cleaned_data['email']
#         user.first_name=self.cleaned_data['first_name']
#         user.last_name=self.cleaned_data['last_name']

#         if commit:
#             user.save()
#         return user

# class StockForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = '__all__'

#         # exclude
#         exclude = ('holder',
#                    'company'
#                    )