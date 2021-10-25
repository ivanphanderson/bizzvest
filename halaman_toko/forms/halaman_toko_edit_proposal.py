from datetime import date

from django.core.exceptions import ValidationError

from models_app.models.Company import *
from django import forms




class CompanyAddProposalForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['proposal']



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'isian-formulir'  # menambahkan class

    def clean(self):
        data = self.cleaned_data

        if (self.instance.status_verifikasi != self.Meta.model.StatusVerifikasi.BELUM_MENGAJUKAN_VERIFIKASI):
            raise ValidationError({"proposal":["Non-zero verfication status cannot change the proposal file"]})

        return data


    def save(self, commit=True):
        self.cleaned_data = dict([ (k,v) for k,v in self.cleaned_data.items() if v != ""])
        return super().save(commit=commit)

