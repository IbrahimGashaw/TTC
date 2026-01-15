# Translation Debugging Guide

## How to Test Translation

1. **Start the server with logging enabled:**
   ```bash
   .\venv\Scripts\python.exe manage.py runserver
   ```

2. **Check the console output** - you should see translation logs like:
   ```
   Translating from en to am: Beautiful apartment...
   Translation successful: ...
   ```

3. **Test in browser:**
   - Go to a property detail page
   - Change language using the language switcher
   - Check if property titles and descriptions translate

## Common Issues

### Issue: Translation not working
- **Check:** Is `deep-translator` installed? Run: `pip list | findstr deep-translator`
- **Check:** Are there errors in the console?
- **Check:** Is the language being set correctly? Check `request.LANGUAGE_CODE` in templates

### Issue: Only language name changes, not content
- **Check:** Is the `translate` filter being used? Look for `{{ property.title|translate }}`
- **Check:** Is `{% load translation_tags %}` at the top of the template?
- **Check:** Check browser console for JavaScript errors

### Issue: Translation is slow
- **Solution:** Translations are cached for 24 hours. First load will be slower.

## Manual Test

To test if translation service works, you can add this to a view temporarily:

```python
from properties.translation_service import get_translation_service
from django.utils.translation import activate

activate('am')  # Set to Amharic
service = get_translation_service()
result = service.translate("Beautiful apartment", 'am', 'en')
print(f"Translation: {result}")
```



