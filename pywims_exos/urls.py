from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.liste_exos, name='liste_exos'),
url(r'^exo/(?P<pk>\d+)/delete/$', views.delete_exo, name='delete_exo'),
url(r'^exo/(?P<pk>\d+)/run/$', views.run_exo, name='run_exo'),
url(r'^exo/(?P<pk>\d+)/corrige/$', views.corrige_exo, name='corrige_exo'),
url(r'^exo/(?P<pk>\d+)/dev/$', views.dev_exo, name='dev_exo'),
]
