"""
Django project package for Team Training and Consultancy Service PLC.
Ensure language codes are registered before URLs are processed.
"""
# This runs when the package is imported, before urls.py
try:
    # Only run if Django is configured
    import os
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        from django.conf import settings
        if hasattr(settings, 'EXTRA_LANG_INFO'):
            import django.conf.locale
            # Register custom language codes in LANG_INFO
            for lang_code, lang_info in settings.EXTRA_LANG_INFO.items():
                django.conf.locale.LANG_INFO[lang_code] = lang_info
            
            # Patch check_for_language to recognize our custom languages
            from django.utils.translation import check_for_language as original_check_for_language
            def patched_check_for_language(lang_code):
                """Patched version that recognizes our custom language codes"""
                if hasattr(settings, 'EXTRA_LANG_INFO') and lang_code in settings.EXTRA_LANG_INFO:
                    return True
                return original_check_for_language(lang_code)
            
            import django.utils.translation
            django.utils.translation.check_for_language = patched_check_for_language
except (ImportError, AttributeError):
    # Django not configured yet, skip
    pass