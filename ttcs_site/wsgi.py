"""
WSGI config for TTCS website.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ttcs_site.settings')

# Apply Python 3.14 compatibility patch
from ttcs_site.compatibility import apply_python314_patch
apply_python314_patch()

application = get_wsgi_application()
