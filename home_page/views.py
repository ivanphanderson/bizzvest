from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

# def add_message(request):
#     form = MessageForm(request.POST or None)
#     if form.is_valid() and request.method == 'POST':
#         form.save()
#         return HttpResponseRedirect('/lab-4')
#     response = {'form': form}
#     return render(request, 'lab4_form.html', response)
