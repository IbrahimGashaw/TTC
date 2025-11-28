"""
Quick script to manually add coordinates to a property.
Run this with: python add_coordinates_quick.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andromedaproperties.settings')
django.setup()

from properties.models import Property

# Find the property
property = Property.objects.get(id=1)  # Achantan,Three BedRoom Apartment

# Coordinates for Ayat, Addis Ababa (approximate - you can get exact from Google Maps)
# To get exact coordinates:
# 1. Go to https://www.google.com/maps
# 2. Search for "Aware Site, Achantan, Ayat, Addis Ababa"
# 3. Right-click on the location
# 4. Click the coordinates that appear
# 5. Copy the numbers and update below

property.latitude = 9.0123  # UPDATE THIS with exact latitude from Google Maps
property.longitude = 38.7890  # UPDATE THIS with exact longitude from Google Maps
property.save()

print(f"✓ Updated '{property.title}'")
print(f"  Coordinates: {property.latitude}, {property.longitude}")
print(f"\nTo get exact coordinates:")
print(f"  1. Go to https://www.google.com/maps")
print(f"  2. Search for: {property.address}, {property.location}, Ethiopia")
print(f"  3. Right-click on the exact location")
print(f"  4. Click the coordinates")
print(f"  5. Update the latitude and longitude in this script")
print(f"  6. Run this script again")


