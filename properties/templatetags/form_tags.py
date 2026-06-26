from django import template
from properties.form_mixins import FIELD_ICONS

register = template.Library()


@register.filter
def field_icon(field_name):
    return FIELD_ICONS.get(field_name, '')
