from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0018_contact_subject_and_labels'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='gdpr_consent',
            field=models.BooleanField(default=False, verbose_name='Privacy Consent'),
        ),
    ]
