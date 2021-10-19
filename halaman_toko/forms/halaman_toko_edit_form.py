from models.models.Company import *
from django import forms

class CompanyEditForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("deskripsi",
                  )

    def save(self, commit=True):
        self.cleaned_data = dict([ (k,v) for k,v in self.cleaned_data.items() if v != "" ])
        return super().save(commit=commit)

