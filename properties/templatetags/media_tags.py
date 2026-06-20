from django import template
from properties.models import embed_video_url as _embed_video_url

register = template.Library()


@register.inclusion_tag('properties/includes/media_gallery.html')
def render_media_gallery(media_items, gallery_id='gallery'):
    return {
        'media_items': media_items,
        'gallery_id': gallery_id,
    }


@register.filter
def embed_video_url(media_item):
    if hasattr(media_item, 'get_embed_video_url'):
        return media_item.get_embed_video_url()
    return None


@register.filter
def embed_url(url):
    return _embed_video_url(url)
