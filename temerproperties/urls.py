"""
Compatibility shim for Andromeda project.
Redirects to the new project's URL configuration.
"""
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from andromedaproperties import urls as andromeda_urls

# Reuse the URL patterns from the new package
urlpatterns = andromeda_urls.urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

