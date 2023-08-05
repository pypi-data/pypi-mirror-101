from django import template
from ..models import Event, Product

register = template.Library()


@register.inclusion_tag('flashday/home.html', takes_context=True)
def flashday(context):
    context.update({
        '_flashday': Event.objects.all()[0],
    })
    return context