from django.db import models

# Create your models here.

class Exo(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    avant = models.TextField()
    enonce = models.TextField()
    apres = models.TextField()
    reponse = models.TextField()

    def __str__(self):
        return self.title