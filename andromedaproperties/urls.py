"""
URL configuration for andromedaproperties project.
"""
from django.contrib import admin
# Customize Django Admin site headers
admin.site.site_header = "Andromeda Admin"
admin.site.site_title = "Andromeda Admin Portal"
admin.site.index_title = "Welcome to Andromeda Administration"
from django.urls import path, include
from django.conf import settings
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

# URL patterns with language prefix
urlpatterns += i18n_patterns(
    path('', include('properties.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from STATICFILES_DIRS in development
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
