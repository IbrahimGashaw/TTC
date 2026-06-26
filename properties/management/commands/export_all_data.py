"""Export all site data to a ZIP archive of Excel files."""
from __future__ import annotations

from datetime import datetime

from django.core.management.base import BaseCommand

from properties.admin_export import build_all_data_zip


class Command(BaseCommand):
    help = 'Export all TTCS database content to a ZIP file of Excel spreadsheets.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            default='',
            help='Output ZIP path (default: ttcs-export-YYYYMMDD.zip in current directory)',
        )

    def handle(self, *args, **options):
        date_stamp = datetime.now().strftime('%Y%m%d')
        output_name = options['output'] or f'ttcs-export-{date_stamp}.zip'

        with open(output_name, 'wb') as output_file:
            output_file.write(build_all_data_zip().getvalue())

        self.stdout.write(self.style.SUCCESS(f'Exported database content to {output_name}'))
