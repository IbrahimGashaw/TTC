"""
Template filters for content sanitization and video URL parsing.
"""
from django import template
from django.utils.safestring import mark_safe
from urllib.parse import urlparse, parse_qs
import re
import bleach

register = template.Library()

# Allowed HTML tags and attributes for content sanitization
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'b', 'i', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre', 'div', 'span', 'hr'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'div': ['class'],
    'span': ['class'],
    'p': ['class'],
    'h1': ['class'],
    'h2': ['class'],
    'h3': ['class'],
    'h4': ['class'],
    'h5': ['class'],
    'h6': ['class'],
    'ul': ['class'],
    'ol': ['class'],
    'li': ['class'],
}

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


@register.filter(name='sanitize_html')
def sanitize_html(value):
    """
    Sanitize HTML content to prevent XSS attacks while allowing safe formatting.
    """
    if not value:
        return ''
    
    # Clean the HTML content
    cleaned = bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )
    
    return mark_safe(cleaned)


@register.filter(name='extract_youtube_id')
def extract_youtube_id(url):
    """
    Extract YouTube video ID from various URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID&t=42s&list=PLAYLIST_ID
    """
    if not url:
        return ''
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Handle youtu.be short URLs
    if 'youtu.be' in parsed.netloc:
        # Extract ID from path: /VIDEO_ID
        video_id = parsed.path.lstrip('/').split('?')[0].split('&')[0]
        return video_id if video_id else ''
    
    # Handle youtube.com URLs
    if 'youtube.com' in parsed.netloc:
        # Try to get from query parameters first (most reliable)
        query_params = parse_qs(parsed.query)
        if 'v' in query_params:
            return query_params['v'][0]
        
        # Try to extract from embed URLs: /embed/VIDEO_ID
        if '/embed/' in parsed.path:
            match = re.search(r'/embed/([a-zA-Z0-9_-]+)', parsed.path)
            if match:
                return match.group(1)
        
        # Try to extract from watch URLs: /watch?v=VIDEO_ID
        if '/watch' in parsed.path:
            match = re.search(r'[?&]v=([a-zA-Z0-9_-]+)', parsed.query or parsed.path)
            if match:
                return match.group(1)
    
    return ''


@register.filter(name='extract_vimeo_id')
def extract_vimeo_id(url):
    """
    Extract Vimeo video ID from various URL formats.
    
    Supports:
    - https://vimeo.com/VIDEO_ID
    - https://player.vimeo.com/video/VIDEO_ID
    - https://vimeo.com/VIDEO_ID?param=value
    """
    if not url:
        return ''
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Handle player.vimeo.com URLs: /video/VIDEO_ID
    if 'player.vimeo.com' in parsed.netloc:
        match = re.search(r'/video/(\d+)', parsed.path)
        if match:
            return match.group(1)
    
    # Handle vimeo.com URLs: /VIDEO_ID
    if 'vimeo.com' in parsed.netloc:
        # Extract numeric ID from path
        match = re.search(r'/(\d+)', parsed.path)
        if match:
            return match.group(1)
    
    return ''

