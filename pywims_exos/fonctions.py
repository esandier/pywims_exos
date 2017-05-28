from sympy import *

def py_wims(a):
# transforme une string en expression sympy, sans la simplifier, renvoie False si echec de conversion.
    with evaluate(False) :
        try: a = sympify(a)
        except (SympifyError, NameError, SyntaxError, IndexError):
            return False
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
# teste l'égalité de deux expressions sympy, après simplification. Utilisation typique: is_equal(py_wims(truc), py_wims(bidule)), donc l'argument est 'false' si la conversion
# a échoué.
    if (a == False) or (b == False) : return False # il y a eu echec de conversion sur a ou b
    else : return  simplify(a-b) == 0

def for_template(arg):
# renvoie arg dans un bon format pour l'affichage dans un template html avec mathjax. Si arg est une liste, s'applique récursivement aux éléments de arg.
    if ('sympy' in str(type(type(arg)))) or  ('sympy' in str(type(arg))): # selon les cas 'sympy' n'est pas dans type(arg), mais dans type(type(arg)). C'est de la cuisine.
        return  r'\displaystyle '+latex(arg, mat_delim="(")        # par défaut l'output latex n'a pas les $, mais est en 'displaystyle'.
    elif type(arg) in [int, float, str] :
        return arg
    elif isinstance(arg, dict):
        return {k: for_template(arg[k]) for k in arg}
    elif isinstance(arg, list):
        return list(map(for_template,arg))
    elif isinstance(arg, tuple):
        return tuple(map(for_template,arg))
    else : return arg
