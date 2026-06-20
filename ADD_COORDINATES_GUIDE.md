# How to Add Coordinates to Properties

## Problem
The map view shows "No properties with location coordinates found" because properties don't have latitude and longitude values set.

## Solution Options

### Option 1: Automatic Geocoding (Recommended)

Use the management command to automatically geocode all properties using Google Geocoding API.

**Step 1: Install requests library (if not already installed)**
```bash
pip install requests
```

**Step 2: Make sure your Google Maps API key is configured**
- The API key should be in `ttcs_site/local_settings.py`
- The same API key works for both Maps JavaScript API and Geocoding API

**Step 3: Enable Geocoding API in Google Cloud Console**
1. Go to https://console.cloud.google.com/
2. Select your project
3. Go to "APIs & Services" > "Library"
4. Search for "Geocoding API"
5. Click "Enable"

**Step 4: Run the geocoding command**

Geocode all properties without coordinates:
```bash
python manage.py geocode_properties
```

Or geocode a specific property:
```bash
python manage.py geocode_properties --property-id 1
```

Or force geocode all properties (even those with coordinates):
```bash
python manage.py geocode_properties --all
```

**Example Output:**
```
Found 5 properties to geocode...
Geocoding: Property Title 1 - Address, Location, Ethiopia... ✓
Geocoding: Property Title 2 - Address, Location, Ethiopia... ✓
...
Geocoding complete!
  Success: 5
  Errors: 0
  Total: 5
```

### Option 2: Manual Entry via Admin

**Step 1: Go to Django Admin**
- Navigate to `/admin/properties/property/`

**Step 2: Edit a Property**
- Click on a property to edit it
- Scroll to the "Location" section
- Enter coordinates manually:
  - **Latitude**: e.g., `9.1450` (for Addis Ababa)
  - **Longitude**: e.g., `38.7614` (for Addis Ababa)

**Step 3: Save**
- Click "Save" to update the property

**Common Coordinates for Ethiopia:**
- **Addis Ababa**: Latitude: 9.1450, Longitude: 38.7614
- **Bahir Dar**: Latitude: 11.6000, Longitude: 37.3833
- **Gondar**: Latitude: 12.6000, Longitude: 37.4667
- **Mekelle**: Latitude: 13.4969, Longitude: 39.4753

### Option 3: Find Coordinates Online

1. Go to https://www.google.com/maps
2. Search for the property address
3. Right-click on the location marker
4. Click on the coordinates that appear (e.g., "9.1450, 38.7614")
5. Copy the latitude and longitude
6. Paste into the admin form

### Option 4: Bulk Update via Django Shell

```python
python manage.py shell
```

Then in the shell:
```python
from properties.models import Property

# Update a specific property
property = Property.objects.get(id=1)
property.latitude = 9.1450
property.longitude = 38.7614
property.save()

# Or update multiple properties
Property.objects.filter(location='Addis Ababa').update(
    latitude=9.1450,
    longitude=38.7614
)
```

## Verify Coordinates

After adding coordinates:

1. Go to Django Admin > Properties
2. Check the "Has Coordinates" column (new column added)
3. Properties with coordinates will show a green checkmark ✓
4. Visit the "Properties With Map" page to see them on the map

## Troubleshooting

**"Geocoding API not enabled" error:**
- Enable Geocoding API in Google Cloud Console (see Option 1, Step 3)

**"API key not valid" error:**
- Check that your API key is correct in `local_settings.py`
- Make sure Geocoding API is enabled for your API key

**"No results found" for an address:**
- Try a more specific address format
- Include city and country (e.g., "Street, Addis Ababa, Ethiopia")
- You may need to manually enter coordinates for that property

**Rate limiting:**
- The command includes a small delay between requests
- If you have many properties, the command may take a few minutes


