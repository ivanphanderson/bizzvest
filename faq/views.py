from django.http import JsonResponse
from django.shortcuts import render
from .forms import NoteForm
from .models import Faq

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
