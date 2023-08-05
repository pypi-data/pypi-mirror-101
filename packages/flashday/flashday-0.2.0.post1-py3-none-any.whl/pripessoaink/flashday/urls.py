from django.urls import include, path

from .views import HomePage, ProductPage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('amuleto/<int:id>', ProductPage.as_view(), name='product')
]
