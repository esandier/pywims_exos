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
        size = kwargs['size']
        matrix = []
        for i in range(size):
            matrix.append([])
            for j in range(size): matrix[i].append('')
    # second method for calling, by specifying numrows and numcols. 
    # Creates a rectangular matrix of blank input fields
    if 'rows' in kwargs and  'cols' in kwargs:
        matrix = []
        for i in range(rows):
            matrix.append([])
            for j in range(cols): matrix[i].append('')
    # third method for calling, by specifying an array.
    # Creates a array of the same size of input fields initialized with the array
    if 'matrix' in kwargs:
        matrix = kwargs['matrix']

    if 'cell_width' in kwargs:
        cell_width = kwargs['cell_width']
    else: cell_width = '2em'
    
    if 'cell_height' in kwargs:
        cell_height = kwargs['cell_height']
    else: cell_height = '2em'
    
    if 'cell_style' in kwargs:
        cell_style = kwargs['cell_style']
    else: cell_style = ''
    
    if 'input_style' in kwargs:
        input_style = kwargs['input_style']
    else: input_style = ''
    
    return {'name': name, 'matrix': matrix, 'cell_style': cell_style, 'input_style': input_style, 'cell_width': cell_width, 'cell_height': cell_height}

# A matrix of input fields which can be user resized
@register.inclusion_tag('pywims_exos/input_vmatrix_ajax.html', takes_context=True)
def input_vmatrix(context, name, **kwargs):

    if 'input_style' in kwargs:
        input_style = kwargs['input_style']
    else: input_style = ''
    
    if 'cell_style' in kwargs:
        cell_style = kwargs['cell_style']
    else: cell_style = ''

    if 'cell_width' in kwargs:
        cell_width = kwargs['cell_width']
    else: cell_width = '2em'
    
    if 'cell_height' in kwargs:
        cell_height = kwargs['cell_height']
    else: cell_height = '2em'
     
    if 'max_rows' in kwargs: 
        max_rows = kwargs['max_rows']
    else: max_rows = 10
        
    if 'max_cols' in kwargs: 
        max_cols = kwargs['max_cols']
    else: max_cols = 10
    
    matrix = []
    for i in range(max_rows):
        matrix.append([])
        for j in range(max_cols): matrix[i].append('')

    return {'name': name, 'matrix':matrix, 'max_rows': max_rows, 'max_cols': max_cols, 'input_style': input_style, 'cell_style': cell_style, 'cell_width': cell_width, 'cell_height': cell_height}

# A matrix of input fields which can be user resized (identical to input-vmatrix, but uses different template)
@register.inclusion_tag('pywims_exos/input_vtable_ajax.html', takes_context=True)
def input_vtable(context, name, **kwargs):

    if 'input_style' in kwargs:
        input_style = kwargs['input_style']
    else: input_style = ''
    
    if 'cell_style' in kwargs:
        cell_style = kwargs['cell_style']
    else: cell_style = ''

    if 'cell_width' in kwargs:
        cell_width = kwargs['cell_width']
    else: cell_width = '2em'
    
    if 'cell_height' in kwargs:
        cell_height = kwargs['cell_height']
    else: cell_height = '2em'
     
    if 'max_rows' in kwargs: 
        max_rows = kwargs['max_rows']
    else: max_rows = 10
        
    if 'max_cols' in kwargs: 
        max_cols = kwargs['max_cols']
    else: max_cols = 10
    
    matrix = []
    for i in range(max_rows):
        matrix.append([])
        for j in range(max_cols): matrix[i].append('')

    return {'name': name, 'matrix':matrix, 'max_rows': max_rows, 'max_cols': max_cols, 'input_style': input_style, 'cell_style': cell_style, 'cell_width': cell_width, 'cell_height': cell_height}

# A set with variable number of elements
@register.inclusion_tag('pywims_exos/input_set_ajax.html', takes_context=True)
def input_set(context, name, **kwargs):

    if 'input_style' in kwargs:
        input_style = kwargs['input_style']
    else: input_style = ''
    
    if 'cell_style' in kwargs:
        cell_style = kwargs['cell_style']
    else: cell_style = ''

    if 'cell_width' in kwargs:
        cell_width = kwargs['cell_width']
    else: cell_width = '2em'
    
    if 'cell_height' in kwargs:
        cell_height = kwargs['cell_height']
    else: cell_height = '2em'
     
    if 'max_elements' in kwargs: 
        max_elements = kwargs['max_elements']
    else: max_elements = 10

    set = ["" for j in range(max_elements)]

    return {'name': name, 'set':set, 'max_elements': max_elements, 'input_style': input_style, 'cell_style': cell_style, 
    'cell_width': cell_width, 'cell_height': cell_height}

@register.inclusion_tag('pywims_exos/input_ggb_ajax.html')
def input_ggb(name):
    return {'name': name}

@register.inclusion_tag('pywims_exos/pw_plot.html')
def pw_plot(plot_data, **kwargs):
    return_data = {'plot_data':plot_data}
    
    if 'width' in kwargs:
        return_data['width'] = kwargs['width']
    else:
        return_data['width'] = 300

    if 'height' in kwargs:
        return_data['height'] = kwargs['height']

    return return_data
    
    
    
    