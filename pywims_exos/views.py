from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect
import json
from .models import Exo
from .fonctions import *
from .forms import ExoForm
from django.core.files import File


def liste_exos(request):
	if request.method == 'GET':
		exos = Exo.objects.all().order_by('title')
		return render(request, 'pywims_exos/liste_exos.html', {'exos': exos})
	if request.method == 'POST':
		status = json.loads(request.body.decode())
		exo = Exo()
		# print(status)
		exo.title = status['title']
		exo.author = request.user
		exo.save()
		return HttpResponse(json.dumps(status), content_type='application/json')

def delete_exo(request, pk):
	exo = get_object_or_404(Exo, pk=pk)
	exo.delete()
	return redirect('liste_exos')

def run_exo_ajax(request, pk):
	if (request.method == 'GET') and (pk != 0) :
		# pk = primary_key de l'exo dans la base de donnée, on le stocke dans le
		# dictionnaire request.session
		exo = get_object_or_404(Exo, pk=pk)
		# On récupère le dictionnaire des variables de l'exo après execution de 'avant'
		# et on le stocke dans request.session
		result = exo.exec_avant({})
		# result['dic'] is the python dictionary resulting from the execution of 'avant'
		# canceled in favor of saving random state 
		#request.session['current_exo_dict'] = result['dic']
		request.session['seed'] = result['seed']
		# result['context'] is a formatted version of result['dic'] suitable for use in a template
		contexte = result['context']
		contexte['current_exo_dict'] = result['dic']
		# on ajoute la primary key de l'exo, utilisée quand on redirige vers la vue 'corrigé'
		contexte['pk'] = pk
		# on ajoute le titre de l'exo, utilisé dans l'affichage
		contexte['exo_title'] = exo.title
		

		string = "{% extends '" + exo.layout_enonce() + "' %}\n {% load input_fields_ajax %}\n"\
		+ '{% block enonce_exo %}\n'+ exo.enonce + '\n{% endblock %}'
		return HttpResponse(Template(string).render(Context(contexte)))

	if request.method == 'POST':
		#print('POST')
		status = json.loads(request.body.decode())
		print('STATUS\n\n',status,'\n\n')

		if status['requested_action'] == 'submit' :
			exo = get_object_or_404(Exo, pk=status['pk'])
			# Les données récupérées après l'exécution de 'avant'. Il faut les récupérer dans un contexte
			# evaluate(False), sinon les expressions sympy peuvent être évaluées, et on ne retrouve pas l'original.
			#with evaluate(False):
				# canceled in favor of restoring random state from seed. 
				#dictionnaire = request.session['current_exo_dict']
			dictionnaire = exo.exec_avant({},seed = request.session['seed'])['dic']

			# add user-input to the dictionary
			# print('FORM DATA\n\n', status['inputs'], '\n\n')
			#for input in status['inputs'] :
			#	dictionnaire[input['name']] = input['value']

			# on ajoute/modifie des données au dictionnaire par l'exécution de 'après'
			# print('DICTIONNAIRE\n\n', dictionnaire, '\n\n')
			result = exo.exec_apres(dictionnaire, status['inputs'])

			# print('RETURNED STATUS\n\n',status,'\n\n')
			return HttpResponse(json.dumps(result), content_type='application/json')

def dev_exo(request, pk):#  affiche la page de développement

	if (request.method == 'GET') and (pk != 0):
		exo = get_object_or_404(Exo, pk=pk)
		block_list = exo.block_info[exo.layout] # la liste des blocs pour ce type d'exo
		status = {'exo': exo.json(), 'current_block' : 'avant', 'langage' : 'python', 'echo' : exo.title}
		return render(request, 'pywims_exos/layout_mode_dev_bootstrap.html',\
		  {'status': status, 'pk':pk, 'LAYOUTS':Exo.EXO_LAYOUTS,\
		   'EMPTY_GGB_FILE':Exo.EXOS_EMPTY_GGB_FILE, 'block_list':block_list})

	if request.method == 'POST':
		print('POST')
		status = json.loads(request.body.decode())

		if (status['requested_action'] == 'preview') or	\
		(status['requested_action'] == 'home') or \
		 (status['requested_action'] == 'update-title') or\
		 (status['requested_action'] == 'update-layout'):
			# print('status   ',status)
			exo = get_object_or_404(Exo, pk=status['exo']['pk'])
			if (status['exo']['layout'] == "GGB") and (status['requested_action'] == 'update-layout') :
				f = open(Exo.EXOS_EMPTY_GGB_FILE)
				exo.ggb_file = File(f)
				f.close()
			exo.assign(status['exo'])
			exo.save()
			status['echo']= exo.title
			return HttpResponse(json.dumps(status), content_type='application/json')
		else :
			return HttpResponse(json.dumps(status), content_type='application/json')

# affiche un formulaire pour les données de l'exo autres que le code
def form_exo(request, pk):
	exo = get_object_or_404(Exo, pk=pk)

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = ExoForm(request.POST, request.FILES, instance = exo)
		form.save()
		return HttpResponseRedirect('/')
		# if a GET (or any other method) we'll display the form
	else:
		form = ExoForm(instance=exo)
		return render(request, 'pywims_exos/form_exo.html', {'form': form, 'pk':pk})
