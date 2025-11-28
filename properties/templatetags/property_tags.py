from django import template
from ..models import SiteSettings

register = template.Library()


@register.simple_tag
def whatsapp_url(property_title=None, message=None):
    """Generate WhatsApp URL with optional property title"""
    site_settings = SiteSettings.load()
    return site_settings.get_whatsapp_url(message=message, property_title=property_title)


@register.simple_tag
def whatsapp_url_simple():
    """Generate simple WhatsApp URL without property info"""
    site_settings = SiteSettings.load()
    return site_settings.get_whatsapp_url()

