from django.shortcuts import render
from .models import Animal

def search(request):
        if request.method == 'POST':
            searched = request.POST['searched']
            animals = Animal.objects.filter(name__contains=searched)
            return render(request, 'searched.html', {'searched': searched, 'animals': animals})
        else:
            return render(request, 'searched.html', {})