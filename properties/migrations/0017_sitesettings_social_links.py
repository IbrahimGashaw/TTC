from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0016_mediaitem_video_file_alter_mediaitem_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='facebook_url',
            field=models.URLField(
                blank=True,
                default='https://www.facebook.com/share/18gfdQKHEu/',
                help_text='Facebook page URL',
                verbose_name='Facebook URL',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='telegram_url',
            field=models.URLField(
                blank=True,
                default='https://t.me/teamconsultency',
                help_text='Telegram channel or group URL',
                verbose_name='Telegram URL',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='youtube_url',
            field=models.URLField(
                blank=True,
                help_text='YouTube channel URL',
                verbose_name='YouTube URL',
            ),
        ),
    ]
