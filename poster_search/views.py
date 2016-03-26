import os
from io import BytesIO
from urllib.request import urlopen

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.files.base import File

import requests

from .models import Poster
from .models import SearchHistory


class PosterView(TemplateView):
    template_name = 'poster.html'

    def get_object(self):

        img_title = self.request.POST['poster-title']

        s = SearchHistory.objects.filter(search_title=img_title).first()

        r = requests.get('http://www.omdbapi.com/?t={}'.format(img_title))

        if 'Poster' in r.json():
            img_url = r.json()['Poster']

            if s:
                if s.poster_name in img_url:
                    # Poster_name on server same as in our storage
                    poster = Poster.objects.filter(poster_url=img_url).first()
                    context['poster'] = poster.image
                    SearchHistory.objects.create(search_title=img_title,
                                                     poster_name = s.poster_name)
                else:
                    # Poster has changed
                    # Download new file and delete the old one
                    poster_image = BytesIO(urlopen(img_url).read())
                    poster = Poster.objects.filter(poster_url=img_url).first()
                    img_name = os.path.split(img_url)[1]
                    poster.image.delete()
                    poster.image.save(img_name, File(poster_image))
                    poster.save()

                    SearchHistory.objects.create(search_title=img_title,
                                                     poster_name = img_name)
                    context['poster'] = poster.image
            else:
                # Poster was not searched previously
                if img_url == 'N/A':
                # Poster is not found on server
                    context['poster_is_na'] = True
                    SearchHistory.objects.create(search_title=img_title,
                                                     poster_name = img_url)
                else:
                    # Download poster for the first time

                    poster_image = BytesIO(urlopen(img_url).read())
                    poster = Poster(poster_url=img_url)
                    img_name = os.path.split(img_url)[1]
                    poster.image.save(img_name, File(poster_image))
                    poster.save()

                    SearchHistory.objects.create(search_title=img_title,
                                                     poster_name = img_name)
                    context['poster'] = poster.image
        else:
            # Movie was not found in omdbapi
            SearchHistory.objects.create(search_title=img_title,
                                         poster_name = 'N/F')


















    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        img_title = self.request.POST['poster-title']

        s = SearchHistory.objects.filter(search_title=img_title).first()

        r = requests.get('http://www.omdbapi.com/?t={}'.format(img_title))

        if 'Poster' in r.json():
            img_url = r.json()['Poster']


            if img_url == 'N/A':
            # Poster is not found on server
                context['poster_is_na'] = True
                SearchHistory.objects.create(search_title=img_title,
                                                 poster_name = img_url)
                return self.render_to_response(context)

            if s:
                if s.poster_name in img_url:
                    # Poster_name on server same as in our storage
                    poster = Poster.objects.filter(poster_url=img_url).first()
                    context['poster'] = poster.image
                    SearchHistory.objects.create(search_title=img_title,
                                                     poster_name = s.poster_name)
                else:
                    # Poster has changed
                    # Download new file and delete the old one
                    poster_image = BytesIO(urlopen(img_url).read())
                    poster = Poster.objects.filter(poster_url=img_url).first()
                    img_name = os.path.split(img_url)[1]
                    poster.image.delete()
                    poster.image.save(img_name, File(poster_image))
                    poster.save()

                    SearchHistory.objects.create(search_title=img_title,
                                                     poster_name = img_name)
                    context['poster'] = poster.image


            else:
                # Poster was not searched previously
                # Download poster for the first time

                poster_image = BytesIO(urlopen(img_url).read())
                poster = Poster(poster_url=img_url)
                img_name = os.path.split(img_url)[1]
                poster.image.save(img_name, File(poster_image))
                poster.save()

                SearchHistory.objects.create(search_title=img_title,
                                                 poster_name = img_name)
                context['poster'] = poster.image
        else:
            # Movie was not found in omdbapi
            SearchHistory.objects.create(search_title=img_title,
                                         poster_name = 'N/F')
            context['poster_is_nf'] = True

        return self.render_to_response(context)


class SearchHistoryView(ListView):

    model = SearchHistory
    template_name = 'history.html'
