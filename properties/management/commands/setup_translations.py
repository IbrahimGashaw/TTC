"""
Management command to set up translation files for Django i18n.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from pathlib import Path
from django.conf import settings


class Command(BaseCommand):
    help = 'Set up translation files for all configured languages'

    def handle(self, *args, **options):
        self.stdout.write('Setting up translation files...')
        
        # Create locale directory if it doesn't exist
        locale_path = Path(settings.BASE_DIR) / 'locale'
        locale_path.mkdir(exist_ok=True)
        
        # Get all language codes from settings
        languages = [lang[0] for lang in settings.LANGUAGES if lang[0] != 'en']
        
        for lang_code in languages:
            self.stdout.write(f'Creating translation files for {lang_code}...')
            try:
                call_command('makemessages', '-l', lang_code, verbosity=0)
                self.stdout.write(self.style.SUCCESS(f'✓ Created translation files for {lang_code}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error creating files for {lang_code}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\nTranslation files setup complete!'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Edit the .po files in locale/<lang>/LC_MESSAGES/django.po')
        self.stdout.write('2. Add translations for each msgid')
        self.stdout.write('3. Run: python manage.py compilemessages')


