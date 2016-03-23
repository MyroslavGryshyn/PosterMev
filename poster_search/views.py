from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse

import requests

from .models import Poster


class PosterView(TemplateView):
    model =  Poster
    template_name = 'poster.html'

    def post(self, *args, **kwargs):
        img_title = self.request.POST['poster']
        img_title.replace(' ', '+')
        r = requests.get('http://www.omdbapi.com/?t={}'.format(img_title))
        img_url = r.json()['Poster']
        return JsonResponse({'img': str(img_url)})
        # return response
