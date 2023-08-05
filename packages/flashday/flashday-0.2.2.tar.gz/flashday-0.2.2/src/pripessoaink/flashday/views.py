from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

from .models import *


class HomePage(TemplateView):
    template_name = "flashday/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flashday = Event.objects.all()[0]
        collections = Collection.objects.filter(event_id=flashday.id) \
                                .prefetch_related('product_set')

        context.update({
            'flashday': flashday,
            'collections': collections
        })

        return context


class ProductPage(TemplateView):
    template_name = 'flashday/product.html'

    @property
    def id(self):
        return self.kwargs['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flashday = Event.objects.all()[0]

        product = Product.objects.filter(id=self.id) \
                         .prefetch_related('productoption_set') \
                         .prefetch_related('extrapicture_set')[0]

        seller = Artist.objects.filter(collection=product.collection.id)[0]

        context.update({
            'flashday': flashday,
            'product': product,
            'seller': seller
        })

        return context


class Home(View):
    def get(self, request):
        return JsonResponse({
            'event': Event.objects.count(),
            'artist': Artist.objects.count(),
            'collection': Collection.objects.count(),
            'product': Product.objects.count(),
        })
