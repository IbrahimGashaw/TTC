"""Context processors to make site settings available globally"""
from .models import SiteSettings
from django.utils.translation import get_language

# PromotionalOffer may not exist
try:
    from .models import PromotionalOffer
except ImportError:
    PromotionalOffer = None


def site_settings(request):
    """Make site settings available in all templates"""
    # Get current language
    current_language = get_language()
    
    # Get promotional offers if model exists
    valid_offers = []
    if PromotionalOffer is not None:
        try:
            active_offers = PromotionalOffer.objects.filter(is_active=True)
            # Filter offers that are currently valid (considering dates)
            valid_offers = [offer for offer in active_offers if offer.is_valid()][:5]  # Limit to 5 offers
        except Exception:
            valid_offers = []
    
    return {
        'site_settings': SiteSettings.load(),
        'CURRENT_LANGUAGE_CODE': current_language,  # Make language code available in templates
        'promotional_offers': valid_offers,
    }

