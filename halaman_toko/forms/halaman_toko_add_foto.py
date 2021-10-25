from models_app.models.CompanyPhoto import *
from django import forms

class CompanyPhotoAddForm(forms.ModelForm):
    class Meta:
        model = CompanyPhoto
        fields = (
            "img",
            # "img_index",  # harus dihandle secara manual oleh server view.py
            # 'company'  # harus dihandle secara manual oleh server view.py
            )

    def clean_img_index(self):
        return self.cleaned_data['company'].companyphoto_set.all().count() + 1

    def form_valid(self, form):
        return super().form_valid(form)

    def save(self, commit=True):
        return super().save(commit=commit)

