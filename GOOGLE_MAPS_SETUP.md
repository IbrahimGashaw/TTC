# Google Maps API Key Setup Guide

## How to Get a Google Maps API Key

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project (or select existing)**
   - Click on the project dropdown at the top
   - Click "New Project"
   - Enter a project name (e.g., "Andromeda Properties")
   - Click "Create"

3. **Enable Required APIs**
   - Go to "APIs & Services" > "Library"
   - Search for and enable:
     - **Maps JavaScript API**
     - **Places API** (optional, for nearby amenities)

4. **Create API Key**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key

5. **Restrict API Key (Recommended for Production)**
   - Click on the created API key to edit it
   - Under "Application restrictions", select "HTTP referrers"
   - Add your website domains (e.g., `yourdomain.com/*`, `localhost:8000/*`)
   - Under "API restrictions", select "Restrict key"
   - Select only "Maps JavaScript API" and "Places API"
   - Click "Save"

## How to Configure the API Key

### Option 1: Environment Variable (Recommended)

**Windows (PowerShell):**
```powershell
$env:GOOGLE_MAPS_API_KEY="YOUR_API_KEY_HERE"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_MAPS_API_KEY=YOUR_API_KEY_HERE
```

**Linux/Mac:**
```bash
export GOOGLE_MAPS_API_KEY="YOUR_API_KEY_HERE"
```

**To make it permanent on Windows:**
1. Open System Properties > Environment Variables
2. Add new User variable:
   - Name: `GOOGLE_MAPS_API_KEY`
   - Value: `YOUR_API_KEY_HERE`

### Option 2: Direct Configuration (Development Only)

Edit `andromedaproperties/settings.py` and uncomment the line:
```python
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY_HERE'
```

⚠️ **Warning:** Never commit API keys to version control!

### Option 3: Create a local_settings.py file

Create a file `andromedaproperties/local_settings.py`:
```python
# Local settings (not in version control)
GOOGLE_MAPS_API_KEY = 'YOUR_API_KEY_HERE'
```

Then add at the end of `andromedaproperties/settings.py`:
```python
try:
    from .local_settings import *
except ImportError:
    pass
```

## Verify Configuration

After setting up the API key, restart your Django development server:
```bash
python manage.py runserver
```

Then visit the "Properties With Map" page to verify the map displays correctly.

## Troubleshooting

- **"Google Maps API key is not configured"**: The API key is not set or empty
- **"This page can't load Google Maps correctly"**: Check if the API key is valid and the required APIs are enabled
- **"RefererNotAllowedMapError"**: Add your domain to the API key restrictions in Google Cloud Console


