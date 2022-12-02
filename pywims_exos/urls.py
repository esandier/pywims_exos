from django.urls import re_path
from django.conf import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
re_path(r'^$', views.liste_exos, name='liste_exos'),
re_path(r'^exo/(?P<pk>\d+)/delete/$', views.delete_exo, name='delete_exo'),
#url(r'^exo/(?P<pk>\d+)/run/$', views.run_exo, name='run_exo'),
re_path(r'^exo/(?P<pk>\d+)/run-ajax/$', views.run_exo_ajax, name='run_exo_ajax'),
#url(r'^exo/(?P<pk>\d+)/corrige/$', views.corrige_exo, name='corrige_exo'),
re_path(r'^exo/(?P<pk>\d+)/dev/$', views.dev_exo, name='dev_exo'),
re_path(r'^exo/(?P<pk>\d+)/form/$', views.form_exo, name='form_exo')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Ajouté pour servir les fichiers FileField
