from django.db import models


class Poster(models.Model):

    poster_url = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='posters', blank=True)


class SearchHistory(models.Model):

    date = models.DateTimeField(auto_now=True)
    search_title = models.CharField(max_length=100)
    poster_url = models.CharField(max_length=2000)

    class Meta:
        ordering = ['-date']
