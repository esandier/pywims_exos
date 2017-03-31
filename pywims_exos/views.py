from django.shortcuts import render
from .models import Exo

def liste_exos(request):
	exos = Exo.objects.all().order_by('title')
	return render(request, 'pywims_exos/liste_exos.html', {'exos': exos})