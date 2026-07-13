from django import template

register = template.Library()


@register.filter
def mul(a, b):
    return a * b


@register.filter
def div(a, b):
    return a / b if b else 0
