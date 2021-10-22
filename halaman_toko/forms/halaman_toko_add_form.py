from models.models.Company import *
from django import forms




class CompanyAddForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ('pemilik_usaha',
                   'nilai_saham_dibutuhkan_total',
                   'nilai_saham_terkumpulkan_total',
                   'start_date',
                   'id',
                   )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'isian-formulir'  # menambahkan class


    def save(self, commit=True):
        self.cleaned_data = dict([ (k,v) for k,v in self.cleaned_data.items() if v != ""])
        return super().save(commit=commit)

