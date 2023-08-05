from django.contrib import admin

from .models import Artist, Collection, Event, ExtraPicture, Product, ProductOption


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'instagram', 'telephone']
    # inlines = ['CollectionInline']

    # class CollectionInline(admin.TabularInline):
    #     model = Collection
    #     extra = 1



# @admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['author']

    def author(self, obj):
        return obj.artist.name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist']
    inlines = ['ProductOptionInline', 'ExtraPictureInline']
    actions = ['change_availability']

    def artist(self, obj):
        return obj.collection.artist.name

    class ExtraPictureInline(admin.TabularInline):
        model = ExtraPicture
        extra = 1

    class ProductOptionInline(admin.TabularInline):
        model = ProductOption
        extra = 1

    def change_availability(self, request, queryset):
        for model in queryset:
            queryset.filter(model.id).update(
                availability=not model.availability
            )


# @admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'product']

    def product(self, obj):
        return obj.reference.title


# @admin.register(ExtraPicture)
class ExtraPictureAdmin(admin.ModelAdmin):
    list_display = ['product']

    def product(self, obj):
        return obj.reference.title

