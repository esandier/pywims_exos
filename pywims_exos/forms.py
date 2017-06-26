from django.forms import ModelForm
from pywims_exos.models import Exo
# Create the form class.
class ExoForm(ModelForm):
    class Meta:
        model = Exo
        fields = ['layout', 'ggb_file']
