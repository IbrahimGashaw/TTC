"""
Translation service for dynamic content translation.
Uses deep-translator library which supports many languages including Amharic, Arabic, etc.
"""
import os
from django.conf import settings
from django.utils.translation import get_language
import logging

logger = logging.getLogger(__name__)

try:
    from django.core.cache import cache
    CACHE_AVAILABLE = True
except Exception:
    CACHE_AVAILABLE = False

try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    logger.warning("deep-translator not installed. Install with: pip install deep-translator")


class TranslationService:
    """Service for translating dynamic content using deep-translator"""
    
    # Language code mapping for deep-translator
    # GoogleTranslator uses simple codes, MyMemoryTranslator uses full locale codes
    LANGUAGE_MAP_GOOGLE = {
        'en': 'en',
        'am': 'am',  # Amharic
        'ar': 'ar',  # Arabic
        'om': 'om',  # Oromo
        'so': 'so',  # Somali
        'ti': 'ti',  # Tigrinya
    }
    
    LANGUAGE_MAP_MYMEMORY = {
        'en': 'en-GB',
        'am': 'am-ET',  # Amharic - Ethiopia
        'ar': 'ar-SA',  # Arabic - Saudi Arabia
        'om': 'om-ET',  # Oromo - Ethiopia
        'so': 'so-SO',  # Somali - Somalia (closest locale)
        'ti': 'ti-ET',  # Tigrinya - Ethiopia
    }
    
    def __init__(self):
        self.cache_timeout = 3600 * 24  # Cache translations for 24 hours
        self.use_cache = True
    
    def translate(self, text, target_language=None, source_language='en'):
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'am', 'ar', 'fr')
            source_language: Source language code (default: 'en')
        
        Returns:
            Translated text or original text if translation fails
        """
        if not TRANSLATION_AVAILABLE:
            return text
        
        if not text or not text.strip():
            return text
        
        if target_language is None:
            target_language = get_language()
        
        # If target is same as source, return original
        if target_language == source_language:
            return text
        
        # If source is not English and target is English, we still want to translate
        # Only skip if both are English
        if target_language == 'en' and source_language == 'en':
            return text
        
        # Check cache first
        if self.use_cache and CACHE_AVAILABLE:
            try:
                cache_key = f"translation_{source_language}_{target_language}_{hash(text)}"
                cached = cache.get(cache_key)
                if cached:
                    return cached
            except Exception as e:
                logger.debug(f"Cache not available: {str(e)}")
        
        try:
            # Map language codes for GoogleTranslator (simple codes)
            source_lang_google = self.LANGUAGE_MAP_GOOGLE.get(source_language, source_language)
            target_lang_google = self.LANGUAGE_MAP_GOOGLE.get(target_language, target_language)
            
            logger.debug(f"Translating from {source_lang_google} to {target_lang_google}: {text[:50]}...")
            
            # Try Google Translator first (more reliable)
            try:
                translator = GoogleTranslator(source=source_lang_google, target=target_lang_google)
                translated = translator.translate(text)
                
                # Check if translation is valid (not empty and different from original)
                if translated and translated.strip():
                    # Cache the result
                    if self.use_cache and CACHE_AVAILABLE:
                        try:
                            cache_key = f"translation_{source_language}_{target_language}_{hash(text)}"
                            cache.set(cache_key, translated, self.cache_timeout)
                        except Exception as e:
                            logger.debug(f"Cache error: {str(e)}")
                    logger.debug(f"Translation successful: {translated[:50]}...")
                    return translated
                else:
                    logger.warning(f"Translation returned empty text, trying fallback")
                    raise Exception("Translation returned empty text")
                    
            except Exception as e:
                logger.debug(f"GoogleTranslator failed: {str(e)}, trying MyMemoryTranslator")
                # Fallback to MyMemoryTranslator (uses full locale codes)
                try:
                    source_lang_mymemory = self.LANGUAGE_MAP_MYMEMORY.get(source_language, source_language)
                    target_lang_mymemory = self.LANGUAGE_MAP_MYMEMORY.get(target_language, target_language)
                    translator = MyMemoryTranslator(source=source_lang_mymemory, target=target_lang_mymemory)
                    translated = translator.translate(text)
                    
                    if translated and translated.strip():
                        if self.use_cache and CACHE_AVAILABLE:
                            try:
                                cache_key = f"translation_{source_language}_{target_language}_{hash(text)}"
                                cache.set(cache_key, translated, self.cache_timeout)
                            except Exception as e:
                                logger.debug(f"Cache error: {str(e)}")
                        logger.debug(f"MyMemory translation successful: {translated[:50]}...")
                        return translated
                    else:
                        logger.debug(f"MyMemoryTranslator returned empty text")
                        return text
                except Exception as e2:
                    logger.debug(f"MyMemoryTranslator failed: {str(e2)}")
                    return text
                
        except Exception as e:
            logger.debug(f"Translation error for {source_language}->{target_language}: {str(e)}")
            return text


# Singleton instance
_translation_service = None

def get_translation_service():
    """Get or create translation service instance"""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service


def translate_text(text, target_language=None, source_language='en'):
    """
    Convenience function to translate text.
    
    Usage in templates:
    {% load translation_tags %}
    {{ property.description|translate }}
    """
    service = get_translation_service()
    return service.translate(text, target_language, source_language)

