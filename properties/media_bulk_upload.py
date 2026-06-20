"""Bulk upload helpers for media albums."""
import os

from django.core.files.base import ContentFile
from django.db.models import Max

from .models import MediaItem


def _next_order(album):
    current = album.items.aggregate(max_order=Max('order'))['max_order']
    return (current or 0) + 1


def _base_title(filename):
    return os.path.splitext(os.path.basename(filename))[0][:200]


def add_bulk_media_to_album(album, uploaded_files):
    """
    Create MediaItem rows from a list of uploaded files.
    Returns the number of items created.
    """
    order = _next_order(album)
    created = 0

    for uploaded in uploaded_files:
        if not uploaded:
            continue

        content_type = (getattr(uploaded, 'content_type', '') or '').lower()
        name = getattr(uploaded, 'name', '') or ''
        extension = os.path.splitext(name)[1].lower()

        is_image = content_type.startswith('image/') or extension in {
            '.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp',
        }
        is_video = content_type.startswith('video/') or extension in {
            '.mp4', '.webm', '.mov', '.avi', '.mkv',
        }

        if is_image:
            MediaItem.objects.create(
                album=album,
                title=_base_title(name),
                media_type='image',
                image=uploaded,
                order=order,
            )
            created += 1
            order += 1
        elif is_video:
            MediaItem.objects.create(
                album=album,
                title=_base_title(name),
                media_type='video',
                video_file=uploaded,
                order=order,
            )
            created += 1
            order += 1

    if created and not album.cover_image:
        first_image = album.items.filter(media_type='image').exclude(image='').first()
        if first_image and first_image.image:
            with first_image.image.open('rb') as source:
                album.cover_image.save(
                    os.path.basename(first_image.image.name),
                    ContentFile(source.read()),
                    save=True,
                )

    return created
