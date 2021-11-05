from datetime import date

from django.core.exceptions import ValidationError

from models_app.models.Company import *
from django import forms




class CompanyAddForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

        # exclude
        exclude = ('pemilik_usaha',
                   'proposal',
                   'status_verifikasi',
                   'start_date',
                   'id',
                   )

        widgets = {
            'end_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'isian-formulir'  # menambahkan class

    def clean(self):
        data = self.cleaned_data

        errors = {}

        if ('jumlah_lembar' not in data or data['jumlah_lembar'] <= 0):
            errors['jumlah_lembar'] = ["jumlah lembar must be positive",]

        if ('nilai_lembar_saham' not in data or data['nilai_lembar_saham'] <= 0):
            errors['nilai_lembar_saham'] = ["nilai lembar saham must be positive",]

        if ('dividen' not in data or data['dividen'] <= 0):
            errors['dividen'] = ["dividen must be positive",]

        if ('end_date' not in data or data['end_date'] <= date.today()):
            errors['end_date'] = ["end date must be in the future",]

        unique_fields = ['kode_saham', 'nama_merek']


        for field in unique_fields:
            if field in data:
                try:
                    Company.objects.get(**{field: data[field]})
                except Company.DoesNotExist:
                    pass
                else:
                    errors[field] = 'Must be unique. Another company has already taken this value.'

        if len(errors) > 0:
            raise ValidationError(errors)

        return data


    def save(self, commit=True):
        self.cleaned_data = dict([ (k,v) for k,v in self.cleaned_data.items() if v != ""])
        return super().save(commit=commit)

