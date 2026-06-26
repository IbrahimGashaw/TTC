from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0017_sitesettings_social_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='subject',
            field=models.CharField(
                choices=[
                    ('general', 'General Inquiry'),
                    ('training', 'Training Programs'),
                    ('consultancy', 'Consultancy Services'),
                    ('hr_sourcing', 'HR Sourcing & Recruitment'),
                    ('events', 'Events & Workshops'),
                    ('partnership', 'Partnership'),
                ],
                default='general',
                max_length=30,
                verbose_name='Subject',
            ),
        ),
        migrations.AlterField(
            model_name='contact',
            name='gdpr_consent',
            field=models.BooleanField(default=False, verbose_name='Privacy Consent'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.TextField(verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=100, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Phone'),
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Contact Message',
                'verbose_name_plural': 'Contact Messages',
            },
        ),
    ]
