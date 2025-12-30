"""
Template tags for translation functionality.
"""
from django import template
from django.utils.translation import get_language, activate
from properties.translation_service import get_translation_service
import logging

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter(name='translate')
def translate_filter(value, target_language=None):
    """
    Template filter to translate text.
    
    Usage:
    {{ property.description|translate }}
    {{ property.title|translate:CURRENT_LANGUAGE_CODE }}
    """
    if not value:
        return value
    
    try:
        # Get current language
        if target_language is None or target_language == 'CURRENT_LANGUAGE_CODE':
            target_language = get_language()
        
        # If still None, default to English (no translation needed)
        if not target_language:
            target_language = 'en'
        
        logger.debug(f"Translation filter: target_lang={target_language}, text='{str(value)[:50]}...'")
        
        # Don't translate if target is English
        if target_language == 'en':
            return value
        
        # Get translation service and translate
        service = get_translation_service()
        result = service.translate(str(value), target_language=target_language, source_language='en')
        
        # Return the result (translated text or original if translation failed)
        return result if result else value
            
    except Exception as e:
        logger.error(f"Translation filter error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return value


@register.simple_tag
def translate_text(text, target_language=None):
    """
    Template tag to translate text.
    
    Usage:
    {% translate_text "Hello" %}
    {% translate_text "Hello" CURRENT_LANGUAGE_CODE %}
    """
    if not text:
        return text
    
    try:
        # Handle the case where target_language is passed as a variable name string
        # If target_language is the string 'CURRENT_LANGUAGE_CODE', try to get actual language
        if target_language == 'CURRENT_LANGUAGE_CODE' or target_language is None:
            target_language = get_language()
        
        # If still None, default to current language
        if not target_language:
            target_language = get_language() or 'en'
        
        logger.debug(f"translate_text tag: target_lang={target_language}, text='{str(text)[:50]}...'")
        
        # Don't translate if target is English
        if target_language == 'en':
            return text
        
        service = get_translation_service()
        result = service.translate(str(text), target_language=target_language, source_language='en')
        
        # Return the result (translated text or original if translation failed)
        return result if result else text
        
    except Exception as e:
        logger.error(f"Translation tag error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return text
