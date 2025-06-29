from django import template

register = template.Library()

@register.filter
def prettify_category(value):
    """Converts 'martial_arts' to 'Martial Arts'."""
    return str(value).replace('_', ' ').title()