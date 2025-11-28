"""Context processors to make site settings available globally"""
from .models import SiteSettings


def site_settings(request):
    """Make site settings available in all templates"""
    return {
        'site_settings': SiteSettings.load()
    }

