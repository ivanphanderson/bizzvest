from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from models_app.models import UserAccount


class RegisterUserForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def clean(self):
		print("cleaning")
		cleaned_data = super().clean()
		username = cleaned_data.get('username')

		for validator in UserAccount.USERNAME_VALIDATORS:
			try:
				print(repr(username))
				validator(username)
			except ValidationError as e:
				self.add_error('username', e.message)
		print("cleaned")
		return cleaned_data

