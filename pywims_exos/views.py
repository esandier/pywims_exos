from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.template import Template, Context
from django.http import HttpResponse
import json
from .models import Exo
from .fonctions import *

#
#
#       Enrobage des exos
#
#

# Des champs de formulaire de type 'input' sont définis pour offrir une interface sympa
# la définition est dans le fichiers input_fields.py, qui réfère à un template par champ
en_tete_exo = """
{% extends "pywims_exos/exo_enonce.html" %}
{% load input_fields %}
{% block enonce_exo %}
"""
# Les champs formulaire de type 'input' sont redéfinis pour l'affichage
# du corrigé : au lieu de champs de formulaire, ils afficheront la réponse de l'utilisateur
# la définition est dans le fichiers input_fields_for_corrige.py, qui réfère à un template par champ
en_tete_corrige = """
{% extends "pywims_exos/exo_corrige.html" %}
{% load input_fields_for_corrige %}
{% block enonce_exo %}
"""
fin_exo = """
{% endblock %}
"""
en_tete_reponse =  """
{% block feedback %}
"""
fin_reponse = """
{% endblock %}
"""

def liste_exos(request):
	if request.method == 'GET':
		exos = Exo.objects.all().order_by('title')
		return render(request, 'pywims_exos/liste_exos.html', {'exos': exos})
	if request.method == 'POST':
		status = json.loads(request.body)
		exo = Exo()
		print(status)
		exo.title = status['title']
		exo.author = request.user
		exo.save()
		return HttpResponse(json.dumps(status), content_type='application/json')

def delete_exo(request, pk):
	exo = get_object_or_404(Exo, pk=pk)
	exo.delete()
	exos = Exo.objects.all().order_by('title')
	return redirect('liste_exos')

def run_exo(request, pk):
	# pk = primary_key de l'exo dans la base de donnée, on le stocke dans le
	# dictionnaire request.session
	exo = get_object_or_404(Exo, pk=pk)
	# On récupère le dictionnaire des variables de l'exo après execution de 'avant'
	# et on le stocke dans request.session
	dictionnaire = exo.exec_avant({})
	request.session['current_exo_dict'] = dictionnaire
	# Le dictionnaire envoyé au template doit être modifié:
	# les expressions sympy sont transformées en Latex par la fonction for_template
	contexte = for_template(dictionnaire)
	contexte['pk'] = pk
	# on ajoute la primary key de l'exo, utilisée quand on redirige vers la vue 'corrigé'

	return HttpResponse(Template(en_tete_exo + exo.enonce + fin_exo).render(Context(contexte)))

def corrige_exo(request, pk):
	# Les données récupérées après l'exécution de 'avant'. Il faut les récupérer dans un contexte
	# evaluate(False), sinon les expressions sympy peuvent être évaluées, et on ne retrouve pas l'original.
	with evaluate(False):
		dictionnaire = request.session['current_exo_dict']

	#print('dictionnaire 2', dictionnaire, '\n\n')
	reverse_form = {}
	form_data = {}

	# on ajoute au dictionnaire les données de formulaire, que l'on conserve séparéments
	# On garde aussi un dictionnaire inversé des données de formulaire, utile pour l'affichage des
	# champs drag-drop
	for v in request.POST :
		dictionnaire[v] = request.POST[v]
		form_data[v] = request.POST[v]
		reverse_form[request.POST[v]] = v

	exo = get_object_or_404(Exo, pk=pk)
	# on ajoute au dictionnaire les données récupérées suite à l'exécution de 'après'
	dictionnaire = exo.exec_apres(dictionnaire)

	ok_answers = dictionnaire['ok_answer']
	contexte = for_template(dictionnaire)
	contexte['form_data'] = form_data
	contexte['reverse_form_data'] = reverse_form
	contexte['answer_data'] = ok_answers
	contexte['pk'] = pk

	return HttpResponse(
		Template(en_tete_corrige + exo.enonce + fin_exo + en_tete_reponse + exo.reponse + fin_reponse)
			.render(Context(contexte))
	)

def dev_exo(request, pk):# TODO : affiche la page de développement

	if (request.method == 'GET') and (pk != 0):
		exo = get_object_or_404(Exo, pk=pk)
		status = {'exo': exo.json(), 'current_code' : 'avant', 'langage' : 'python', 'echo' : exo.title}
		return render(request, 'pywims_exos/layout_mode_dev.html', {'status': status, 'pk':pk})

	if request.method == 'POST':
		print('POST')
		status = json.loads(request.body)

		if status['requested_action'] == 'preview':
			print('PREVIEW')
			exo = get_object_or_404(Exo, pk=status['exo']['pk'])
			exo.assign(status['exo'])
			exo.save()
			status['echo']= exo.title
			return HttpResponse(json.dumps(status), content_type='application/json')

		elif status['requested_action'] == 'save':
			print('SAVE_FILE')
			exo = get_object_or_404(Exo, pk=status['exo']['pk'])
			exo.assign(status['exo'])
			exo.save()
			status['echo'] = 'File saved'
			return HttpResponse(json.dumps(status), content_type='application/json')

		elif status['requested_action'] == 'save_as':
			print('SAVE_AS')
			new_exo = Exo()
			new_exo.assign(status['exo'])
			new_exo.title = status['title']
			new_exo.save()
			status['echo'] = new_exo.title
			return HttpResponse(json.dumps(status), content_type='application/json')
		else :
			return HttpResponse(json.dumps(status), content_type='application/json')
