# Translation Setup Guide

This project uses a combination of Django i18n for static content and deep-translator for dynamic content translation.

## Features

- **Automatic Translation**: Dynamic content (property titles, descriptions) is automatically translated using the `deep-translator` library
- **Multi-language Support**: Supports English, Amharic (አማርኛ), Arabic (العربية), and French (Français)
- **Caching**: Translations are cached for 24 hours to improve performance
- **Template Filters**: Easy-to-use template filters for translating content

## How It Works

### 1. Static Content (Django i18n)
For static text in templates (buttons, labels, etc.), use Django's `{% trans %}` tag:

```django
{% load i18n %}
{% trans "View Details" %}
```

### 2. Dynamic Content (Translation Service)
For dynamic content from the database (property titles, descriptions), use the `translate` filter:

```django
{% load translation_tags %}
{{ property.title|translate }}
{{ property.description|translate|linebreaks }}
```

## Usage in Templates

### Property Detail Page
```django
{% load translation_tags %}
<h1>{{ property.title|translate }}</h1>
<p>{{ property.description|translate|linebreaks }}</p>
```

### Property List Page
```django
{% load translation_tags %}
{% for property in properties %}
    <h3>{{ property.title|translate }}</h3>
    <p>{{ property.description|translate|truncatewords:20 }}</p>
{% endfor %}
```

## Translation Service

The translation service uses `deep-translator` which:
- Supports 100+ languages including Amharic, Arabic, French
- Works without API keys (free tier)
- Automatically caches translations
- Falls back gracefully if translation fails

## Language Codes

- `en` - English
- `am` - Amharic (አማርኛ)
- `ar` - Arabic (العربية)
- `fr` - French (Français)

## Testing Translation

1. Change the language using the language switcher in the navbar
2. Property titles and descriptions should automatically translate
3. Static text (buttons, labels) will use Django i18n translations

## Notes

- Translations are cached for 24 hours
- If translation fails, the original text is returned
- The service automatically detects the current language from Django's language settings



