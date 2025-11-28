# How to Enable Geocoding API

## Error Message
```
This API project is not authorized to use this API.
```

## Solution: Enable Geocoding API

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Make sure you're logged in with the same Google account that created the API key
3. Select the **same project** that your API key belongs to

### Step 2: Navigate to API Library
1. Click on the hamburger menu (☰) in the top left
2. Go to **"APIs & Services"** > **"Library"**
   - Or directly visit: https://console.cloud.google.com/apis/library

### Step 3: Enable Geocoding API
1. In the search bar, type: **"Geocoding API"**
2. Click on **"Geocoding API"** from the results
3. Click the blue **"Enable"** button
4. Wait a few seconds for it to enable

### Step 4: Verify API is Enabled
1. Go to **"APIs & Services"** > **"Enabled APIs"**
2. You should see **"Geocoding API"** in the list

### Step 5: Wait and Retry
- Sometimes it takes 1-2 minutes for the API to be fully activated
- Wait a minute, then run the command again:
  ```bash
  python manage.py geocode_properties
  ```

## Alternative: Quick Enable Link

If you're logged into Google Cloud Console, you can use this direct link:
- **Geocoding API**: https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com

Just click "Enable" on that page.

## Important Notes

1. **Same Project**: Make sure the Geocoding API is enabled in the **same project** where your API key was created
2. **Billing**: Geocoding API has a free tier (first $200/month free), but you may need to enable billing on your Google Cloud project
3. **API Key Restrictions**: If your API key has restrictions, make sure "Geocoding API" is allowed in the API restrictions

## Check API Restrictions (if needed)

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click on your API key
3. Under **"API restrictions"**, make sure:
   - Either "Don't restrict key" is selected, OR
   - "Restrict key" is selected AND "Geocoding API" is in the allowed list

## After Enabling

Once enabled, run the geocoding command again:
```bash
python manage.py geocode_properties
```

You should see success messages (✓) instead of errors.


