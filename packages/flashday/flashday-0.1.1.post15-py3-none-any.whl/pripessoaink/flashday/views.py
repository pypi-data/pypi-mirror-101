from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import *


class Home(View):
    def get(self, request):
        return JsonResponse({
            'event': Event.objects.count(),
            'artist': Artist.objects.count(),
            'collection': Collection.objects.count(),
            'product': Product.objects.count(),
        })
