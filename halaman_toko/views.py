from django.shortcuts import render

# Create your views here.


def index(req):
    return render(req, "halaman_toko.html", {
        'nama_merek':        'Toko Emas Rawamangun',
        'nama_perusahaan':  'PT. emas sejahtera',
    })