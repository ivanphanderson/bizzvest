from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import NoteForm
from .models import Faq
from django.core import serializers
import json

def index(request):
    form = NoteForm()
    pertanyaan = Faq.objects.all()
    response = {'form': form, 'tanya': pertanyaan}
    return render(request, 'faq_index.html', response)

def save_data(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            nama = request.POST['nama']
            pertanyaan = request.POST['pertanyaan']
            faq = Faq(nama=nama, pertanyaan=pertanyaan)
            faq.save()
            tanya = Faq.objects.values()
            pertanyaan_data = list(tanya)
            return JsonResponse({'status':'Save', 'pertanyaan_data': pertanyaan_data})
        else:
            return JsonResponse({'status':0})

@csrf_exempt
def faqJson(request):
    if(request.method == 'POST'):
        print(request.body)
        data = json.loads(request.body)
        faq = Faq(nama=data['nama'], pertanyaan=data['pertanyaan'])
        faq.save()
    pertanyaan = Faq.objects.all()
    dataPertanyaan = serializers.serialize('json', pertanyaan)
    dataPertanyaan = json.loads(dataPertanyaan)
    return JsonResponse(dataPertanyaan, safe=False)
