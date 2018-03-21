﻿from django.db import models
from django.conf import settings
from django.template import Template, Context
import os

from sympy import *
from random import *
import  math
from .fonctions import *
#from django.core.files import File


def execution(code_string, dictionnaire, inputs=[], declarations = []):
# executes  python code "code_string", after assigning variables in  'dictionnaire', a dictionary, 
# and in 'inputs', which is a list of pairs {'id': id, 'value':value}. This allows more flexibility in variable assignments, for instance
# {'id':'a[1]', 'value':37}
# puis renvoie un dictionnaire de toutes les variables locales (définies dans 'dictionnaire' et définies par 'code_string')
    class Code:
        def __init__(self, dictionnaire, inputs):
            # for declarations, 'value' must be executed as a python statement
            # not put between quotes to make a string value
            for v in declarations:
                exec(v['id']+'='+v['value'])
            # dictionnaire is made available as python variables
            for v in dictionnaire : 
                exec(v+'=dictionnaire["'+v+'"]')
            # for inputs, the 'id' is executed as a python statement, useful for assignements like 'a[1] = something'
            # the right-hand side is the 'value', put between quotes.
            for i in inputs: 
                exec(i['id']+'='+ '"'+i['value']+'"')
            exec(code_string)
            self.variables = locals()
            del self.variables['dictionnaire'], self.variables['inputs'], self.variables['declarations'], self.variables['self'], self.variables['code_string']
            
            print(inputs)
    code = Code(dictionnaire, inputs)
    return code.variables

# Create your models here.

class Exo(models.Model):
    # les fichiers layout pour chaque type d'exo
    layouts_enonce = {'STD': 'layout_standard_ajax.html', 'GGB': 'layout_geogebra_ajax.html'}
    layouts_corrige = {'STD': 'layout_standard_corrige.html', 'GGB': 'layout_geogebra_corrige.html'}
    # les types d'exos
    EXO_LAYOUTS = (('STD', 'Standard'), ('GGB', 'Geogebra'))
    EXOS_EMPTY_GGB_FILE = os.path.join(settings.MEDIA_ROOT,'ggb_files/empty.ggb')
    # infos sur les blocs utiles à l'éditeur
    block_info = {
        'STD' : [
            {'name': 'avant', 'label': 'Avant', 'langage':'python'},
            {'name': 'enonce', 'label': 'Enoncé', 'langage':'django'},
            {'name': 'apres', 'label': 'Après', 'langage':'python'},
            {'name': 'reponse', 'label': 'Réponse', 'langage':'django'}],
        'GGB' : [
            {'name': 'avant', 'label': 'Avant', 'langage':'python'},
            {'name': 'ggb_commands', 'label': 'Geogebra', 'langage':'django'},
            {'name': 'enonce', 'label': 'Enoncé', 'langage':'django'},
            {'name': 'apres', 'label': 'Après', 'langage':'python'},
            {'name': 'reponse', 'label': 'Réponse', 'langage':'django'}]}
    # layout de l'exo. Pour l'instant 'standard' ou 'geogebra'
    layout = models.CharField(max_length=3, choices=EXO_LAYOUTS, default = 'STD')
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    # Fichier geogebra qui contient la construction initiale
    ggb_file = models.FileField(upload_to = 'ggb_files', blank = True, default = '')
    # contient le code Python exécuté avant le rendu de l'exo. En particulier génère les
    # éléments 'random' de l'exo.
    avant = models.TextField(blank = True, default = '')
    # Pour les exos geogebra, contient les commandes de construction, utile pour les parties random
    # de la construction, et pour définir les variables que retourne l'applet geogebra en guise d'input.
    ggb_commands = models.TextField(blank = True, default = '')
    # Template qui décrit le formulaire de l'exo, les champs réponse.
    enonce = models.TextField(blank = True, default = '')
    # Code Python exécuté après validation du formulaire. Décide si c'est juste ou faux
    # et définit le feedback
    apres = models.TextField(blank = True, default = '')
    # Template qui affiche le feedback.
    reponse = models.TextField(blank = True, default = '')

    def layout_enonce(self): # renvoie le nom du fichier layout_enonce
        return settings.LAYOUTS_DIRECTORY+'/'+self.layouts_enonce[self.layout]

    def layout_corrige(self): # renvoie le nom du fichier layout_corrige
        return settings.LAYOUTS_DIRECTORY+'/'+self.layouts_corrige[self.layout]

    def exec_avant(self, dictionnaire):
        result = {}
        # dictionary of variabes set by 'avant' code
        result['dic'] = execution(self.avant, dictionnaire)
        # the template context gets a formatted version ...
        result['context'] = for_template(result['dic'])

        # addition for geogebra layout: ... and some geogebra data, if present
        if self.layout == 'GGB':
            result['context']['ggb_commands'] = self.exec_ggb(result['dic'])
            result['context']['ggb_file'] = self.ggb_file
            
        return result

    def exec_apres(self, dic, inputs):
        # flattens inputs into a single list of pairs {'id:id,'value':value'} not grouped by type
        # this is what is expected by 'execution'
        inputs_list = []
        for type in inputs :
            # le type 'dec' correspond à une déclaration de variable, la 'value' 
            # doit être interprétée comme une déclaration python, pas comme une string à mettre entre quotes
            if type != 'dec':
                for input in inputs[type] : inputs_list.append(input)
        # On ajoute comme variable le dictionnaire 'ok_answer', qui peut ête renseigné dans le corrigé
        dic['ok_answer'] = {}
        # on ajoute/modifie des données au dictionnaire par l'exécution de 'après'
        # print('DICTIONNAIRE\n\n', dictionnaire, '\n\n')
        if 'dec' in inputs : dic = execution(self.apres, dic, inputs_list, inputs['dec'])
        else : dic = execution(self.apres, dic, inputs_list)
        ok_answer = dic['ok_answer']
        print(ok_answer)
        
        #for input in status['inputs'] :
        for type in inputs :
            for input in inputs[type] :
                if (input['id'] in ok_answer) and (ok_answer[input['id']] == True) :
                    input['style'] = "good_answer"
                # except for geogebra objects, not good means wrong
                else : 
                    input['style'] = "wrong_answer"
        # addition for geogebra layout
        if 'ggb' in inputs:
            for input in inputs['ggb'] :
                    if (input['id'] in ok_answer) and (ok_answer[input['id']] == True) :
                        input['style'] = "good_answer"
                    elif (input['id'] in ok_answer) and (ok_answer[input['id']] == False) :
                        input['style'] = "wrong_answer"
                    # for geogebra objects, not good means nothing (otherwise most would be wrong)
                    else: input['style'] = "other"
        print(inputs)        
        result = {}
        result['feedback'] = Template(self.reponse).render(Context(for_template(dic)))
        result['inputs'] = inputs

        return result
        
        
        
    # renvoie les commandes geogebra avec les variables python remplacées par leurs valeurs
    # il faut enlever les lignes blanches qui provoquent un message d'erreur dans l'applet geogebra
    def exec_ggb(self, dictionnaire):
        commandes = Template(self.ggb_commands).render(Context(dictionnaire))
        commandes = os.linesep.join([s for s in commandes.splitlines() if s])
        return commandes
    # permet de copier dans l'exo une variable python.
    def assign(self, object):
        for key in object :
            if hasattr(self, key): setattr(self, key, object[key])
    # renvoie le contenu de l'objet sous forme d'un dictionnaire.
    # A MODIFIER QUAND LE MODELE CHANGE
    def json(self):
        return {'pk': self.pk, 'title': self.title, 'avant': self.avant,
        'layout': self.layout,
        'ggb_commands': self.ggb_commands, 'enonce': self.enonce,
        'apres': self.apres, 'reponse': self.reponse, 'block_info': self.block_info}

    def __str__(self):
        return self.title

            
            