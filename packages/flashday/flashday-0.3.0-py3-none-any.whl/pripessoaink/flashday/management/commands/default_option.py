from django.core.management.base import BaseCommand, CommandError
from pripessoaink.flashday.models import Product


class Command(BaseCommand):
    help = 'Set product default options'

    def add_arguments(self, parser):
        parser.add_argument('option', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        try:
            for product in Product.objects.filter(productoption__isnull=True):
                for key in kwargs['option']:
                    product.productoption_set.create(
                        key=key
                    )
        except Exception:
            raise CommandError('Something went wrong')

        self.stdout.write(self.style.SUCCESS('Successfully set product prices'))
