"""
Django settings for Team Training and Consultancy Service PLC website.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ttcs-development-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Google Maps API Key (set in environment variable or override in local settings)
# Option 1: Set environment variable: export GOOGLE_MAPS_API_KEY='your-api-key-here'
# Option 2: Set directly below (for development only - not recommended for production)
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
# Uncomment and add your API key below for development:
# GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY_HERE'


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'properties.apps.PropertiesConfig',
    'blog.apps.BlogConfig',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'properties.middleware.LanguageDetectionMiddleware',  # Custom language detection (before LocaleMiddleware)
    'django.middleware.locale.LocaleMiddleware',  # Add locale middleware for i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ttcs_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'properties.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'ttcs_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Africa/Addis_Ababa'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages
LANGUAGES = [
    ('en', 'English'),
    ('am', 'አማርኛ'),  # Amharic - official working language, ~29.3% of population
    ('ar', 'العربية'),  # Arabic
    ('om', 'Oromoo'),  # Oromo - most widely spoken native language, ~33.8% of population
    ('so', 'Soomaali'),  # Somali - ~6.25% of Ethiopian population
    ('ti', 'ትግርኛ'),  # Tigrinya - ~5.86% of Ethiopian population
]

# Extra language info for languages not in Django's default list
# Must include all required keys that Django expects
EXTRA_LANG_INFO = {
    'am': {
        'bidi': False,
        'code': 'am',
        'name': 'Amharic',
        'name_local': 'አማርኛ',
    },
    'om': {
        'bidi': False,
        'code': 'om',
        'name': 'Oromo',
        'name_local': 'Oromoo',
    },
    'so': {
        'bidi': False,
        'code': 'so',
        'name': 'Somali',
        'name_local': 'Soomaali',
    },
    'ti': {
        'bidi': False,
        'code': 'ti',
        'name': 'Tigrinya',
        'name_local': 'ትግርኛ',
    },
}

# Add extra language info to Django's language info
# This must be done before Django processes URLs
import django.conf.locale
from django.utils.translation import gettext_lazy as _

# Merge our custom language info with Django's default
# We need to ensure these are in LANG_INFO before i18n_patterns is called
for lang_code, lang_info in EXTRA_LANG_INFO.items():
    django.conf.locale.LANG_INFO[lang_code] = lang_info

# Also patch check_for_language to recognize our custom languages
# This ensures i18n_patterns will accept these language codes
from django.utils.translation import check_for_language as original_check_for_language
def patched_check_for_language(lang_code):
    """Patched version that recognizes our custom language codes"""
    if lang_code in EXTRA_LANG_INFO:
        return True
    return original_check_for_language(lang_code)

# Monkey patch check_for_language
import django.utils.translation
django.utils.translation.check_for_language = patched_check_for_language

# Also patch get_supported_language_variant to recognize our custom languages
# This is used by get_language_from_path which is critical for URL routing
from django.utils.translation.trans_real import get_supported_language_variant as original_get_supported_language_variant
import functools

@functools.lru_cache(maxsize=1000)
def patched_get_supported_language_variant(lang_code, strict=False):
    """Patched version that recognizes our custom language codes"""
    # First check if it's one of our custom languages
    if lang_code in EXTRA_LANG_INFO:
        # Verify it's in settings.LANGUAGES
        lang_codes = [code for code, name in LANGUAGES]
        if lang_code in lang_codes:
            return lang_code
    # Fall back to original implementation
    return original_get_supported_language_variant(lang_code, strict=strict)

# Monkey patch get_supported_language_variant
import django.utils.translation.trans_real
django.utils.translation.trans_real.get_supported_language_variant = patched_get_supported_language_variant

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Cache configuration for translation service
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'translation-cache',
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'properties.translation_service': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'properties.templatetags.translation_tags': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Allow larger image and video uploads (50 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email Configuration
# For development: emails will be printed to console
# For production: configure SMTP settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Prints to console
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'  # Saves to files
# EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'  # For file backend

# Production SMTP settings (uncomment and configure for production)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  # or your SMTP server
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'
# DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
# SERVER_EMAIL = 'your-email@gmail.com'

# Django Jazzmin Configuration
JAZZMIN_SETTINGS = {
    # Title on the brand (19 chars max)
    "site_title": "TTCS Admin",
    
    # Title on the login screen (19 chars max)
    "site_header": "TTCS Portal",
    
    # Title on the brand when screen is at < 1200px (19 chars max)
    "site_brand": "TTCS Admin",
    
    "site_logo": "images/team-training-logo.jpg",
    "login_logo": "images/team-training-logo.jpg",
    "site_logo_classes": "elevation-3",
    
    "site_icon": "images/team-training-logo.jpg",
    
    # Welcome text on the login screen
    "welcome_sign": "Team Training & Consultancy — Admin Login",
    
    # Copyright on the footer
    "copyright": "Team Training and Consultancy Service PLC",
    
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": ["properties.Service", "properties.TrainingEvent", "blog.BlogPost"],
    
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    
    ############
    # Top Menu #
    ############
    
    # Links to put along the top menu
    "topmenu_links": [
        {"name": "View Website", "url": "/", "new_window": True},
    ],
    
    #############
    # User Menu #
    #############
    
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "View Site", "url": "/", "new_window": True},
        {"model": "auth.user"}
    ],
    
    #############
    # Side Menu #
    #############
    
    # Whether to display the side menu
    "show_sidebar": True,
    
    # Whether to aut expand the menu
    "navigation_expanded": True,
    
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    
    "order_with_respect_to": [
        "properties.Service",
        "properties.TrainingEvent",
        "properties.EventRegistration",
        "properties.CaseStudy",
        "properties.TeamMember",
        "properties.Testimonial",
        "properties.Partner",
        "properties.MediaAlbum",
        "properties.Milestone",
        "properties.Contact",
        "properties.HomePageSettings",
        "properties.SiteSettings",
        "properties.WorkingSchedule",
        "blog.BlogPost",
        "blog.BlogCategory",
        "auth",
    ],
    
    # Custom links to append to app groups, keyed on app name
    "custom_links": {},
    
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1 for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "properties.Service": "fas fa-briefcase",
        "properties.TrainingEvent": "fas fa-chalkboard-teacher",
        "properties.EventRegistration": "fas fa-user-check",
        "properties.CaseStudy": "fas fa-chart-line",
        "properties.Testimonial": "fas fa-quote-left",
        "properties.Partner": "fas fa-handshake",
        "properties.TeamMember": "fas fa-user-tie",
        "properties.MediaAlbum": "fas fa-images",
        "properties.Contact": "fas fa-envelope",
        "properties.Milestone": "fas fa-flag",
        "properties.WorkingSchedule": "fas fa-clock",
        "properties.HomePageSettings": "fas fa-home",
        "properties.SiteSettings": "fas fa-cog",
        "properties.MediaItem": "fas fa-photo-video",
        "properties.CaseStudyTimeline": "fas fa-stream",
        "blog.BlogPost": "fas fa-blog",
        "blog.BlogCategory": "fas fa-tags",
        "properties": "fas fa-globe",
        "blog": "fas fa-newspaper",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "css/admin_ttcs.css",
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    
    ###############
    # Change view #
    ###############
    # Render change forms as collapsible sections to avoid tab JS quirks in some setups
    "changeform_format": "collapsible",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}


# Load local settings if available (for development overrides)
try:
    from .local_settings import *
except ImportError:
    pass
