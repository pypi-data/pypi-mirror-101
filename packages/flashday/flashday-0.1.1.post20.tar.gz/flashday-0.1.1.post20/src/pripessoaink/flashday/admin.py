from django.contrib import admin

from .models import Artist, Collection, Event, ExtraPicture, Product, ProductOption


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    fields = ['name', 'instagram', 'telephone']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['artist']

    def artist(self, obj):
        return obj.artist.name


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist']

    def artist(self, obj):
        return obj.collection.artist.name

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
    list_display = ['key', 'value', 'product']

    def product(self, obj):
        return obj.reference.name


@admin.register(ExtraPicture)
class ExtraPictureAdmin(admin.ModelAdmin):
    list_display = ['product']

    def product(self, obj):
        return obj.reference.name

