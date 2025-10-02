"""
Auto migration to add post_logout_redirect_uris field to Application if missing.

This migration is added to ensure the database schema contains the
post_logout_redirect_uris column required by the project's oauth models
and initialization scripts. It's intentionally idempotent when run on
databases that already have the column.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0003_application_post_logout_redirect_uris_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='post_logout_redirect_uris',
            field=models.TextField(blank=True, help_text='Allowed Post Logout URIs list, space separated'),
            preserve_default=True,
        ),
    ]
