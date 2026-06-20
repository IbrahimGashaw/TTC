"""
URL configuration for Team Training and Consultancy Service PLC website.
"""
from django.contrib import admin
# Customize Django Admin site headers
admin.site.site_header = "Team Training & Consultancy"
admin.site.site_title = "TTCS Admin"
admin.site.index_title = "Website Management Dashboard"

# IMPORTANT: Patch language validation functions BEFORE importing i18n_patterns
# This ensures custom language codes are recognized for URL routing
from django.conf import settings
if hasattr(settings, 'EXTRA_LANG_INFO'):
    import django.conf.locale
    import functools
    # Register custom language codes in LANG_INFO
    for lang_code, lang_info in settings.EXTRA_LANG_INFO.items():
        django.conf.locale.LANG_INFO[lang_code] = lang_info
    
    # Patch check_for_language to recognize our custom languages
    from django.utils.translation import check_for_language as original_check_for_language
    def patched_check_for_language(lang_code):
        """Patched version that recognizes our custom language codes"""
        if lang_code in settings.EXTRA_LANG_INFO:
            return True
        return original_check_for_language(lang_code)
    
    import django.utils.translation
    django.utils.translation.check_for_language = patched_check_for_language
    
    # Patch get_supported_language_variant to recognize our custom languages
    # This is critical for get_language_from_path which is used by LocaleMiddleware
    from django.utils.translation.trans_real import get_supported_language_variant as original_get_supported_language_variant
    
    @functools.lru_cache(maxsize=1000)
    def patched_get_supported_language_variant(lang_code, strict=False):
        """Patched version that recognizes our custom language codes"""
        # First check if it's one of our custom languages
        if lang_code in settings.EXTRA_LANG_INFO:
            # Verify it's in settings.LANGUAGES
            lang_codes = [code for code, name in settings.LANGUAGES]
            if lang_code in lang_codes:
                return lang_code
        # Fall back to original implementation
        return original_get_supported_language_variant(lang_code, strict=strict)
    
    import django.utils.translation.trans_real
    django.utils.translation.trans_real.get_supported_language_variant = patched_get_supported_language_variant

from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from django.http import FileResponse
import os

def serve_favicon(request):
    """Serve favicon.ico from static files"""
    static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.BASE_DIR / 'static'
    favicon_path = os.path.join(static_dir, 'favicon.ico')
    if os.path.exists(favicon_path):
        return FileResponse(open(favicon_path, 'rb'), content_type='image/x-icon')
    else:
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound()

# Import the custom language view directly
from properties.views import custom_set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('favicon.ico', serve_favicon),
    # Custom language switcher - must be outside i18n_patterns
    path('set-language/', custom_set_language, name='custom_set_language'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URL patterns with language prefix
urlpatterns += i18n_patterns(
    path('', include('properties.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
