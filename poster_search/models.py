from django.db import models


class Poster(models.Model):

    url = models.CharField(max_length=2000)
    image = models.ImageField()
