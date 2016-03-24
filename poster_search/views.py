import os
from io import BytesIO
from urllib.request import urlopen

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.core.files.base import File

import requests

from .models import Poster


class PosterView(TemplateView):
    template_name = 'poster.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        img_title = self.request.POST['poster-title']
        img_title.replace(' ', '+')

        r = requests.get('http://www.omdbapi.com/?t={}'.format(img_title))
        if 'Poster' in r.json():
            img_url = r.json()['Poster']
            poster_image = BytesIO(urlopen(img_url).read())
            poster = Poster(poster_url=img_url)
            img_name = os.path.split(img_url)[1]
            poster.image.save(img_name, File(poster_image))
            poster.save()
            context['poster'] = img_name
            # if Poster.objects.filter(poster_url=img_url):

        return self.render_to_response(context)
