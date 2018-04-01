from sympy import *
from django.template import Template, Context


# added for plots
import matplotlib
matplotlib.use('agg')
matplotlib.rcParams['savefig.dpi'] = 80
matplotlib.rcParams['figure.figsize'] = (4,3)
matplotlib.rcParams['savefig.transparent'] = True
from io import BytesIO
import base64
# end of addition for plots


def py_wims(a):
# transforme une string en expression sympy, sans la simplifier, renvoie None si echec de conversion.
    with evaluate(False) :
        try: a = sympify(a)
        except (SympifyError, NameError, SyntaxError, IndexError):
            return None
        return a

def is_nombre(a):
# détermine si a est un nombre, avant même évaluation/simplification
    number_types = [int, float, numbers.Catalan, numbers.EulerGamma, numbers.Exp1, \
        numbers.Float, numbers.Half, numbers.ImaginaryUnit, numbers.Integer, numbers.NegativeOne, numbers.One, numbers.Pi]
    return type(a) in number_types

def is_fraction(a):
# détermine si, sans simplification,  une  expression sympy est une fraction, au sens de : un nombre divisé par un autre
    f = fraction(a)
    return (is_nombre(f[0]) and  is_nombre(f[1]))

def is_equal(a, b):
# teste l'égalité de deux expressions sympy, après simplification. Utilisation typique: 
# is_equal(py_wims(truc), py_wims(bidule)), donc l'argument est 'None' si la conversion
# a échoué.
    if (a == None) or (b == None) : return None # il y a eu echec de conversion sur a ou b
    else : return  simplify(a-b) == 0


def for_template(arg):
# returns arg in a format suitable for use in an html template with mathjax. applies recursively to list items if arg is a list
    x = symbols('x')
    graphe = plot(x, show=False)
    
    if type(arg) == type(graphe): # Case of a plot. An html  image tag is returned.
        figfile = BytesIO()
        arg.save(figfile)
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = base64.b64encode(figfile.getvalue())
        figfile.close()
    
        context = {'plot_data': figdata_png}
        return  Template('<img src="data:image/png;base64,{{ plot_data }}" style="pointer-events:none">').render(Context(context))
    elif isinstance(arg, tuple(core.all_classes)): # tests for a sympy expression
        return  r'\displaystyle '+latex(arg, mat_delim="[") # delault latex output doesn't include $, but enforces 'displaystyle'.
    elif type(arg) in [int, float, str] :
        return arg
    elif isinstance(arg, dict):
        return {k: for_template(arg[k]) for k in arg}
    elif isinstance(arg, list):
        return list(map(for_template,arg))
    elif isinstance(arg, tuple):
        return tuple(map(for_template,arg))
    else : return arg
