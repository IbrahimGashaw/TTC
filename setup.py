#!/usr/bin/env python
"""
Quick setup script for Andromeda Properties Django project.
Run this after installing dependencies to set up the database.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andromedaproperties.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("Setting up Andromeda Properties...")
    print("1. Making migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    print("2. Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    print("3. Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the server: python manage.py runserver")
    print("3. Visit http://127.0.0.1:8000/")

