"""
WSGI config for Andromedaproperties project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andromedaproperties.settings')

# Apply Python 3.14 compatibility patch
from andromedaproperties.compatibility import apply_python314_patch
apply_python314_patch()

application = get_wsgi_application()
