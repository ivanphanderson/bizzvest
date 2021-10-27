from django import template

register = template.Library()

@register.filter
def index(sequence, pos):
    return sequence[pos]