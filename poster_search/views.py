import os
from io import BytesIO
from urllib.request import urlopen

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.core.files.base import File

import requests

from .models import Poster
from .models import SearchHistory


class PosterView(TemplateView):

    template_name = 'poster.html'

    @staticmethod
    def save_image(img_url, context, img_title, poster_url=''):
        if poster_url:
            poster = Poster.objects.filter(poster_url=poster_url).first()
            poster.image.delete()
        else:
            poster = Poster(poster_url=img_url)

        poster_image = BytesIO(urlopen(img_url).read())
        img_name = os.path.split(img_url)[1]
        poster.image.save(img_name, File(poster_image))
        poster.save()

        SearchHistory.objects.create(search_title=img_title,
                                     poster_url=img_url)
        return poster.image

    def post(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)

        img_title = self.request.POST['poster-title']
        r = requests.get('http://www.omdbapi.com/?t={}'.format(img_title))

        if 'Poster' in r.json():
            # Movie is found on server
            img_url = r.json()['Poster']

            if img_url == 'N/A':
                # Poster is not found on server
                context['poster_is_na'] = True
                SearchHistory.objects.create(search_title=img_title,
                                             poster_url=img_url)
                return self.render_to_response(context)

            search = SearchHistory.objects. \
                filter(search_title=img_title).first()

            if search:
                # We've looked for this title before
                if search.poster_url == img_url:
                    # Poster_url on server is same as in our db
                    poster = Poster.objects.filter(poster_url=img_url).first()
                    context['poster'] = poster.image
                    SearchHistory.objects.create(search_title=img_title,
                                                 poster_url=img_url)
                else:
                    # Poster has changed - download new and delete the old file
                    context['poster'] = self.save_image(img_url, img_title,
                                                        search.poster_url)
            else:
                # Download poster for the first time
                context['poster'] = self.save_image(img_url, context,
                                                    img_title)
        else:
            # Movie was not found on server
            SearchHistory.objects.create(search_title=img_title,
                                         poster_url='N/F')
            context['poster_is_nf'] = True

        return self.render_to_response(context)


class SearchHistoryView(ListView):

    model = SearchHistory
    template_name = 'history.html'
