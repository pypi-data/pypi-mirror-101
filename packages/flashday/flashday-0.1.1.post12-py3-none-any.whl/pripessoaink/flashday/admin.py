from django.contrib import admin

from .models import Artist, Collection, Event, ExtraPicture, Product, ProductOption


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    fields = ['name', 'instagram', 'telefone']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['artist']


@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['artist']

    class ExtraPictureInline(admin.TabularInline):
        model = ExtraPicture

    class ProductOptionInline(admin.TabularInline):
        model = ProductOption

    inlines = [
        ExtraPictureInline,
        ProductOptionInline,
    ]


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']


@admin.register(ExtraPicture)
class ExtraPictureAdmin(admin.ModelAdmin):
    list_display = ['reference']

