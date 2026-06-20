from django import template
from ..models import SiteSettings

register = template.Library()


@register.simple_tag
def whatsapp_url(subject=None, message=None):
    """Generate WhatsApp URL with optional inquiry subject."""
    site_settings = SiteSettings.load()
    return site_settings.get_whatsapp_url(message=message, subject=subject)


@register.simple_tag
def whatsapp_url_simple():
    """Generate simple WhatsApp URL without extra context."""
    site_settings = SiteSettings.load()
    return site_settings.get_whatsapp_url()
