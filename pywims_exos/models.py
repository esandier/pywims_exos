from django.db import models
from sympy import *
from random import *
import  math
from .fonctions import *


def execution(code_string, dictionnaire):
# execute le code python contenu dans "code_string", après avoir renseigné les variables présentes dans 'dictionnaire',
# puis renvoie un dictionnaire de toutes les variables locales (définies dans 'dictionnaire' et définies par 'code_string')
	class Code:
		def __init__(self, dictionnaire):
			for v in dictionnaire : exec(v+'=dictionnaire["'+v+'"]')
			exec(code_string)
			self.variables = locals()
			del self.variables['dictionnaire'], self.variables['self'], self.variables['code_string']

	code = Code(dictionnaire)
	return code.variables

# Create your models here.

class Exo(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	avant = models.TextField('')
	enonce = models.TextField('')
	apres = models.TextField('')
	reponse = models.TextField('')

	def exec_avant(self, dictionnaire):
		return execution(self.avant, dictionnaire)

	def exec_apres(self, dictionnaire):
		# On ajoute comme variable le dictionnaire 'ok_answer', qui peut ête renseigné dans le corrigé
		dictionnaire['ok_answer'] = {}
		return execution(self.apres, dictionnaire)

	def assign(self, object):
	# permet de copier dans l'exo une variable python.
		for key in object :
			if hasattr(self, key): setattr(self, key, object[key])

	def json(self):
		return {'pk': self.pk, 'title': self.title, 'avant': self.avant,
		'enonce': self.enonce, 'apres': self.apres, 'reponse': self.reponse}

	def __str__(self):
		return self.title
