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

@register.inclusion_tag('pywims_exos/input_matrix_ajax.html', takes_context=True)
def input_matrix(context, name, **kwargs):
    # first way of calling, by specifying a size. Creates a square matrix of blank input fields
    if 'size' in kwargs:
        range_lines = range(kwargs['size'])
        range_cols = range_lines
        matrix = []
        for i in range_lines:
            matrix.append([])
            for j in range_cols: matrix[i].append('')
    # second method for calling, by specifying numlines and numcols. 
    # Creates a rectangular matrix of blank input fields
    if 'lines' in kwargs and  'cols' in kwargs:
        range_lines = range(kwargs['lines'])
        range_cols = range(kwargs['cols'])
        matrix = []
        for i in range_lines:
            matrix.append([])
            for j in range_cols: matrix[i].append('')
    # third method for calling, by specifying an array.
    # Creates a array of the same size of input fields initialized with the array
    if 'matrix' in kwargs:
        matrix = kwargs['matrix']
        range_lines = range(len(matrix))
        range_cols = range(len(matrix[0]))

    if 'style_cell' in kwargs:
        style_cell = kwargs['style_cell']
    else: style_cell = ''
    
    # lines and cols are put in a range because django templates dont do numeric loops
    return {'name': name, 'matrix': matrix, 'range_lines': range_lines,'range_cols':range_cols, 'style_cell': style_cell}

@register.inclusion_tag('pywims_exos/input_ggb_ajax.html')
def input_ggb(name):
    return {'name': name}
