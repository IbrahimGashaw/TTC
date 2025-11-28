"""
Custom middleware for automatic language detection and redirection.
Integrates with browser language preferences and Google language detection.
"""
from django.utils import translation
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import resolve, Resolver404
import re


class LanguageDetectionMiddleware:
    """
    Middleware that automatically detects user's language preference and redirects
    to the appropriate language version of the page.
    
    Features:
    - Detects browser language from Accept-Language header
    - Respects user's manual language selection (session/cookie)
    - Automatically redirects to correct language URL on first visit
    - Works with prefix_default_language=False
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.supported_languages = [lang[0] for lang in settings.LANGUAGES]
        self.default_language = settings.LANGUAGE_CODE
        self.lang_prefixes = [lang for lang in self.supported_languages if lang != 'en']
        
    def __call__(self, request):
        # Skip language detection for certain paths
        skip_paths = ['/admin/', '/static/', '/media/', '/favicon.ico', '/set-language/', '/i18n/']
        if any(request.path.startswith(path) for path in skip_paths):
            return self.get_response(request)
        
        # Get current language from session (set by language switcher)
        current_lang = request.session.get('django_language') or translation.get_language()
        
        # Check if user has manually selected a language (has session)
        manual_selection = request.session.get('django_language') is not None
        
        # Parse current path to detect if it has a language prefix
        path = request.path
        detected_lang = None
        path_without_lang = path
        
        # Check if path starts with a language prefix
        for lang_prefix in self.lang_prefixes:
            prefix_pattern = '/' + lang_prefix + '/'
            if path.startswith(prefix_pattern):
                detected_lang = lang_prefix
                path_without_lang = '/' + path[len(prefix_pattern):]
                break
            elif path == '/' + lang_prefix:
                detected_lang = lang_prefix
                path_without_lang = '/'
                break
        
        # If no language prefix in URL and default language, path stays as is
        if detected_lang is None:
            detected_lang = 'en'
        
        # On first visit (no manual selection), detect from browser
        if not manual_selection and not request.session.get('language_detected'):
            browser_lang = self.detect_browser_language(request)
            
            # If browser language matches a supported language and differs from current
            if browser_lang and browser_lang != detected_lang and browser_lang in self.supported_languages:
                # Build redirect URL to browser's preferred language
                # Use path_without_lang to get clean path, then add appropriate prefix
                redirect_url = self.build_language_url(path_without_lang, browser_lang)
                
                # Add query string if exists
                if request.GET:
                    redirect_url += '?' + request.GET.urlencode()
                
                # Only redirect if URL actually changes
                current_full_path = request.get_full_path()
                if redirect_url != current_full_path:
                    # Mark that we've detected language for this session
                    request.session['language_detected'] = True
                    request.session['django_language'] = browser_lang
                    request.session.modified = True
                    return HttpResponseRedirect(redirect_url)
            else:
                # Mark that we've detected language (using default)
                request.session['language_detected'] = True
        
        # Set language for this request
        if current_lang and current_lang in self.supported_languages:
            translation.activate(current_lang)
        
        response = self.get_response(request)
        
        # Reset to default language after request
        translation.deactivate()
        
        return response
    
    def detect_browser_language(self, request):
        """
        Detect user's preferred language from browser Accept-Language header.
        Returns the best matching supported language code or None.
        """
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        
        if not accept_language:
            return None
        
        # Parse Accept-Language header (e.g., "en-US,en;q=0.9,ar;q=0.8")
        languages = []
        for lang_item in accept_language.split(','):
            lang_item = lang_item.strip()
            if ';' in lang_item:
                lang_code, q_value = lang_item.split(';', 1)
                try:
                    q = float(q_value.split('=')[1])
                except (ValueError, IndexError):
                    q = 1.0
            else:
                lang_code = lang_item
                q = 1.0
            
            # Extract primary language code (e.g., "en-US" -> "en")
            lang_code = lang_code.split('-')[0].lower()
            
            if lang_code in self.supported_languages:
                languages.append((lang_code, q))
        
        # Sort by quality (q value)
        languages.sort(key=lambda x: x[1], reverse=True)
        
        # Return the best matching language
        if languages:
            return languages[0][0]
        
        return None
    
    def build_language_url(self, path, language):
        """
        Build URL with appropriate language prefix.
        For English (default), no prefix. For others, add prefix.
        """
        # Normalize path
        if not path.startswith('/'):
            path = '/' + path
        
        if path == '/':
            path = ''
        
        # Build URL based on language
        if language == 'en':
            # English: no prefix
            url = '/' + path.lstrip('/')
        else:
            # Other languages: add prefix
            if not path or path == '/':
                url = '/' + language + '/'
            else:
                url = '/' + language + path
        
        # Remove double slashes
        url = re.sub(r'/+', '/', url)
        
        # Ensure it doesn't end with multiple slashes (except root)
        if url != '/' and url.endswith('//'):
            url = url.rstrip('/') + '/'
        
        return url

