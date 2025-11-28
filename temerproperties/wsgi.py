"""
Compatibility shim for Andromeda project.
This file redirects to the new settings package so older references still work.
"""

import os
from django.core.wsgi import get_wsgi_application

# Ensure the environment points to the new settings package
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andromedaproperties.settings')

application = get_wsgi_application()

