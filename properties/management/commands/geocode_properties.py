"""
Management command to geocode property addresses and add latitude/longitude coordinates.
Uses Google Geocoding API to convert addresses to coordinates.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from properties.models import Property
import requests
import time


class Command(BaseCommand):
    help = 'Geocode property addresses to get latitude and longitude coordinates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-key',
            type=str,
            help='Google Maps API key (or use GOOGLE_MAPS_API_KEY from settings)',
        )
        parser.add_argument(
            '--property-id',
            type=int,
            help='Geocode a specific property by ID',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Geocode all properties without coordinates',
        )

    def handle(self, *args, **options):
        api_key = options.get('api_key') or getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
        
        if not api_key:
            self.stdout.write(
                self.style.ERROR('Google Maps API key not found. Set GOOGLE_MAPS_API_KEY in settings or use --api-key option.')
            )
            return

        if options.get('property_id'):
            properties = Property.objects.filter(id=options['property_id'])
        elif options.get('all'):
            properties = Property.objects.filter(
                latitude__isnull=True,
                longitude__isnull=True
            ) | Property.objects.filter(latitude=0, longitude=0)
        else:
            # Default: geocode properties without coordinates
            properties = Property.objects.filter(
                latitude__isnull=True,
                longitude__isnull=True
            ) | Property.objects.filter(latitude=0, longitude=0)
            if not properties.exists():
                self.stdout.write(
                    self.style.WARNING('No properties found without coordinates. Use --all to geocode all properties.')
                )
                return

        total = properties.count()
        self.stdout.write(f'Found {total} properties to geocode...')

        success_count = 0
        error_count = 0

        for property in properties:
            # Build address string
            address = f"{property.address}, {property.location}, Ethiopia"
            
            self.stdout.write(f'Geocoding: {property.title} - {address}...', ending=' ')
            
            try:
                # Call Google Geocoding API
                url = 'https://maps.googleapis.com/maps/api/geocode/json'
                params = {
                    'address': address,
                    'key': api_key
                }
                
                response = requests.get(url, params=params, timeout=10)
                data = response.json()
                
                if data['status'] == 'OK' and data['results']:
                    location = data['results'][0]['geometry']['location']
                    property.latitude = location['lat']
                    property.longitude = location['lng']
                    property.save()
                    success_count += 1
                    self.stdout.write(self.style.SUCCESS('✓'))
                elif data['status'] == 'REQUEST_DENIED':
                    error_count += 1
                    error_msg = data.get('error_message', 'API not authorized')
                    self.stdout.write(self.style.ERROR(f'✗ ({error_msg})'))
                    self.stdout.write(self.style.WARNING(
                        '\n  → SOLUTION: Enable "Geocoding API" in Google Cloud Console:\n'
                        '    1. Go to https://console.cloud.google.com/apis/library\n'
                        '    2. Search for "Geocoding API"\n'
                        '    3. Click "Enable"\n'
                        '    4. Wait a few minutes for activation\n'
                        '    5. Run this command again\n'
                    ))
                else:
                    error_count += 1
                    error_msg = data.get('error_message', data.get('status', 'Unknown error'))
                    self.stdout.write(self.style.ERROR(f'✗ ({error_msg})'))
                
                # Rate limiting - be nice to the API
                time.sleep(0.2)
                
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'✗ ({str(e)})'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Geocoding complete!'))
        self.stdout.write(f'  Success: {success_count}')
        self.stdout.write(f'  Errors: {error_count}')
        self.stdout.write(f'  Total: {total}')

