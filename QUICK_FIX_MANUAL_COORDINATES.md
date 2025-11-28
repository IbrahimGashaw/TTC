# Quick Fix: Add Coordinates Manually

While you're setting up the Geocoding API, you can manually add coordinates to get the map working immediately.

## Option 1: Via Django Admin (Easiest)

1. **Go to Django Admin**
   - Visit: http://127.0.0.1:8000/admin/properties/property/
   - Login if needed

2. **Find Your Property**
   - Look for "Achantan,Three BedRoom Apartment"
   - Click on it to edit

3. **Add Coordinates**
   - Scroll down to the "Location" section
   - You'll see fields for:
     - Location: (already filled)
     - Address: (already filled)
     - **Latitude**: Enter `9.1450` (or find exact coordinates)
     - **Longitude**: Enter `38.7614` (or find exact coordinates)

4. **Find Exact Coordinates for Ayat, Addis Ababa**
   - Go to: https://www.google.com/maps
   - Search for: "Ayat, Addis Ababa, Ethiopia"
   - Right-click on the location
   - Click the coordinates that appear (e.g., "9.0123, 38.7890")
   - Copy the first number (latitude) and second number (longitude)
   - Paste into the admin form

5. **Save**
   - Click "Save" at the bottom
   - The property will now appear on the map!

## Option 2: Via Django Shell

```bash
python manage.py shell
```

Then run:
```python
from properties.models import Property

# Find the property
property = Property.objects.get(title__icontains="Achantan")

# Set coordinates for Ayat, Addis Ababa (approximate)
# You can get exact coordinates from Google Maps
property.latitude = 9.0123  # Replace with exact latitude
property.longitude = 38.7890  # Replace with exact longitude
property.save()

print(f"Updated {property.title} with coordinates: {property.latitude}, {property.longitude}")
```

## Option 3: Find Exact Coordinates Online

1. **Using Google Maps:**
   - Go to: https://www.google.com/maps
   - Search for: "Aware Site, Achantan, Ayat, Addis Ababa, Ethiopia"
   - Right-click on the exact location
   - Click the coordinates (e.g., "9.0123, 38.7890")
   - The first number is **Latitude**
   - The second number is **Longitude**

2. **Using LatLong.net:**
   - Go to: https://www.latlong.net/
   - Search for the address
   - Copy the coordinates

## Common Coordinates for Ethiopia Locations

- **Addis Ababa (City Center)**: 9.1450, 38.7614
- **Ayat Area (Approximate)**: 9.0123, 38.7890
- **Bole Area**: 9.0100, 38.7800
- **Cazanchis**: 9.0200, 38.7500

**Note:** These are approximate. For best results, find the exact coordinates using Google Maps.

## Verify It Works

After adding coordinates:
1. Go to: http://127.0.0.1:8000/properties/?view=map
2. You should see your property on the map!


