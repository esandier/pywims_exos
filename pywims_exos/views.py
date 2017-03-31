from django.shortcuts import render

def liste_exos(request):
	return render(request, 'pywims_exos/liste_exos.html', {})