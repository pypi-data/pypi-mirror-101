import re

from django.core.management.base import BaseCommand, CommandError
from pripessoaink.flashday.models import ProductOption


def map_type(arg_value, pat=re.compile(r"[a-zA-Z]+:[0-9]+$")):
    if not pat.match(arg_value):
        raise ValueError

    key, value = arg_value.split(':')
    return key, int(value)


class Command(BaseCommand):
    help = 'Set product option value'

    def add_arguments(self, parser):
        parser.add_argument('mapping', nargs='+', type=map_type)

    def handle(self, *args, **kwargs):
        try:
            for key, value in kwargs['mapping']:
                ProductOption.objects\
                    .filter(key__startswith=key)\
                    .update(value=value)
        except Exception:
            raise CommandError('Something went wrong')

        self.stdout.write(self.style.SUCCESS('Successfully set product prices'))
