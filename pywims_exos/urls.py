from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.liste_exos, name='liste_exos'),
]