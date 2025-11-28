# Detailed Guide: Enable Geocoding API

## Step-by-Step with Screenshots Description

### Step 1: Access Google Cloud Console
1. Go to: https://console.cloud.google.com/
2. **Make sure you're logged in** with the same Google account that created your API key
3. **Select the correct project** from the project dropdown at the top
   - This is CRITICAL - it must be the same project where your API key was created

### Step 2: Navigate to API Library
**Method A (Direct Link):**
- Click: https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com
- This takes you directly to the Geocoding API page

**Method B (Manual Navigation):**
1. Click the hamburger menu (☰) in the top-left corner
2. Hover over "APIs & Services"
3. Click "Library"

### Step 3: Search and Enable Geocoding API
1. In the search bar at the top, type: **"Geocoding API"**
2. You should see "Geocoding API" in the results
3. Click on **"Geocoding API"** (it should show the Google logo)
4. On the API details page, click the blue **"ENABLE"** button
5. Wait 10-30 seconds for it to enable
6. You should see a green checkmark or "API enabled" message

### Step 4: Verify API is Enabled
1. Go to: https://console.cloud.google.com/apis/dashboard
2. Scroll down to "Enabled APIs & services"
3. Look for **"Geocoding API"** in the list
4. If you see it, you're good to go!

### Step 5: Check API Key Restrictions (Important!)

1. Go to: https://console.cloud.google.com/apis/credentials
2. Find your API key in the list (it might be named or just show as "API key")
3. **Click on the API key** to edit it
4. Scroll down to **"API restrictions"** section
5. You have two options:

   **Option A: No Restrictions (Easiest)**
   - Select **"Don't restrict key"**
   - Click "Save"
   - This allows the key to use all enabled APIs

   **Option B: Restrict Key (More Secure)**
   - Select **"Restrict key"**
   - Under "Select APIs", make sure **"Geocoding API"** is checked
   - Also check **"Maps JavaScript API"** (for the map display)
   - Click "Save"

### Step 6: Wait and Test
1. **Wait 1-2 minutes** for changes to propagate
2. Run the geocoding command again:
   ```bash
   python manage.py geocode_properties
   ```
3. You should now see success (✓) instead of errors!

## Troubleshooting

### "Still getting authorization error"
- **Double-check the project**: Make sure you enabled the API in the SAME project as your API key
- **Check API restrictions**: Your API key must allow Geocoding API
- **Wait longer**: Sometimes it takes 2-5 minutes for changes to take effect
- **Try a different browser**: Clear cache or use incognito mode

### "Can't find my API key"
1. Go to: https://console.cloud.google.com/apis/credentials
2. Look for keys with type "API key"
3. If you have many keys, check the "Created" date
4. You can also create a new API key specifically for this project

### "Billing required"
- Google Cloud requires billing to be enabled (even for free tier)
- Go to: https://console.cloud.google.com/billing
- Link a billing account (you won't be charged if you stay within free tier)
- Free tier: $200/month credit, which covers thousands of geocoding requests

### "API enabled but still not working"
1. **Check API key in local_settings.py**: Make sure it's correct
2. **Restart Django server**: Sometimes settings need a restart
3. **Check API quotas**: Go to APIs & Services > Dashboard > Geocoding API > Quotas
4. **Try the direct API test**: 
   ```bash
   curl "https://maps.googleapis.com/maps/api/geocode/json?address=Addis+Ababa&key=YOUR_API_KEY"
   ```

## Quick Test Command

After enabling, test with a single property:
```bash
python manage.py geocode_properties --property-id 1
```

Replace `1` with your property ID.


