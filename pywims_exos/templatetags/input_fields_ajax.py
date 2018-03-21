from django import template

register = template.Library()

@register.inclusion_tag('pywims_exos/input_text_ajax.html')
def input_text(name, **kwargs):
    if 'style' in kwargs:
        style_string = kwargs['style']
    else: style_string = ''

    return {'name': name,  'style': style_string}

@register.inclusion_tag('pywims_exos/input_select_ajax.html')
def input_select(name, liste, **kwargs):
    if 'style' in kwargs:
        style_string = kwargs['style']
    else: style_string = ''

    return  {'name': name,  'liste': liste, 'style': style_string}

@register.inclusion_tag('pywims_exos/input_drag_ajax.html')
def input_drag(name, display, **kwargs):
    if 'style_contenu' in kwargs:
        style_contenu_string = kwargs['style_contenu']
    else: style_contenu_string = ''

    if 'style_boite' in kwargs:
        style_boite_string = kwargs['style_boite']
    else: style_boite_string = ''

    return {'name': name, 'display': display, 'style_boite': style_boite_string,
    'style_contenu': style_contenu_string}

@register.inclusion_tag('pywims_exos/input_drop_ajax.html')
def input_drop(name, display, **kwargs):
    if 'style_contenu' in kwargs:
        style_contenu_string = kwargs['style_contenu']
    else: style_contenu_string = ''

    if 'style_boite' in kwargs:
        style_boite_string = kwargs['style_boite']
    else: style_boite_string = ''

    return {'name': name, 'display': display, 'style_boite': style_boite_string,
    'style_contenu': style_contenu_string}

@register.inclusion_tag('pywims_exos/input_matrix_ajax.html')
def input_matrix(name, lines, colonnes, **kwargs):
    if 'style_cell' in kwargs:
        style_cell_string = kwargs['style_cell']
    else: style_cell_string = ''
    
    # lines and cols are put in a range because django templates dont do numeric loops
    return {'name': name, 'rangelines': range(lines), 'rangecols': range(colonnes), 'style_cell': style_cell_string}

@register.inclusion_tag('pywims_exos/input_ggb_ajax.html')
def input_ggb(name):
    return {'name': name}
