from django.db import models


class Poster(models.Model):

    poster_url = models.CharField(max_length=2000)
    image = models.ImageField(upload_to = 'poster_search/static/posters', blank=False)
