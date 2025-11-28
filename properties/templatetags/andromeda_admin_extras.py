from django import template
from django.apps import apps

register = template.Library()


@register.simple_tag
def model_count(app_label, model_name):
    """Return the total count for the given model. Returns 0 on error."""
    try:
        Model = apps.get_model(app_label, model_name)
        if Model is None:
            return 0
        return Model.objects.count()
    except Exception:
        return 0
