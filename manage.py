#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andromedaproperties.settings')
    try:
        from django.core.management import execute_from_command_line
        # Apply Python 3.14 compatibility patch after Django is imported
        from andromedaproperties.compatibility import apply_python314_patch
        apply_python314_patch()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

