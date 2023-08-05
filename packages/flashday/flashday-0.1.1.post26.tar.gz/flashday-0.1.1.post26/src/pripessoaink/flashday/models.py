from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    ImageField,
    Model,
    TextField,
)


class Event(Model):
    title = CharField(max_length=50)
    description = TextField()
    image = ImageField(upload_to='event')

    def __str__(self):
        return self.title


class Artist(Model):
    name = CharField(max_length=50)
    description = TextField()
    instagram = CharField(max_length=50)
    telephone = CharField(max_length=13)
    picture = ImageField(upload_to='artist')

    def __str__(self):
        return self.name


class Collection(Model):
    artist = ForeignKey(Artist, on_delete=CASCADE)

    def __str__(self):
        return self.artist.name


class Product(Model):
    collection = ForeignKey(Collection, on_delete=CASCADE)
    title = CharField(max_length=50)
    description = TextField()
    availability = BooleanField(default=True)
    picture = ImageField(upload_to='product')

    actions = ['change_availability']

    def change_availability(self, request, queryset):
        for model in queryset:
            queryset.filter(model.id).update(
                availability=not model.availability
            )

    def __str__(self):
        return self.title


class ProductOption(Model):
    reference = ForeignKey(Product, on_delete=CASCADE)
    key = CharField(max_length=50)
    value = CharField(max_length=50)

    def __str__(self):
        return self.key


class ExtraPicture(Model):
    reference = ForeignKey(Product, on_delete=CASCADE)
    image = ImageField(upload_to='product')

    def __str__(self):
        return self.image.name
