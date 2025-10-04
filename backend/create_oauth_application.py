#!/usr/bin/env python
"""
Script to create OAuth2 application for the student information system.
Run this script after setting up the database.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.temp')
django.setup()

from oauth2_provider.models import Application
from oauth.models import User
from django.core.management import call_command
from django.db.utils import ProgrammingError
import os

def create_oauth_application():
    """Create OAuth2 application if it doesn't exist"""
    
    # Try to run migrations if table doesn't exist
    try:
        Application.objects.count()
    except ProgrammingError:
        print("⚠️ Running migrations...")
        # Make sure oauth migrations directory exists
        oauth_migrations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'oauth', 'migrations')
        if not os.path.exists(oauth_migrations_dir):
            os.makedirs(oauth_migrations_dir)
            
        # Create initial migration for oauth if not exists
        oauth_initial_migration = os.path.join(oauth_migrations_dir, '0001_initial.py')
        if not os.path.exists(oauth_initial_migration):
            with open(oauth_initial_migration, 'w') as f:
                f.write("""from django.db import migrations

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('oauth2_provider', '0001_initial'),
    ]

    operations = []
""")
                
        # Run migrations
        call_command('migrate')
    
    client_id = os.getenv('BUSINESS_CLIENT_ID', 'ejnIx2wsSw73lvJrGAO3CXO111SikplyDPJ9BdEn')
    client_secret = os.getenv('BUSINESS_CLIENT_SECRET', 'kUVb7jaAkWcDt9nOjes89SpLmNPRG99VNnRuonudxmxPLGRQEd1fuFzaeBHAQXKvDt6DAE3jheNYZVUFPDOM9lyon399WTdz5thETiHxsZXKAHe59Q1vKAo9E0KGl61f')

    # Get or create superuser
    try:
        user = User.objects.get(email='quynhtruong272@gmail.com')
    except User.DoesNotExist:
        print("⚠️ Superuser not found. Please run create_default_accounts.py first")
        return

    # Check if application exists
    if Application.objects.filter(client_id=client_id).exists():
        print(f"⚠️ OAuth2 application with client_id {client_id} already exists")
        return

    # Create application
    application = Application.objects.create(
        name='Student Management System',
        user=user,
        client_id=client_id,
        client_secret=client_secret,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
        skip_authorization=True
    )

    print(f"✅ Created OAuth2 application: {application.name}")
    print(f"🔑 Client ID: {application.client_id}")
    print(f"🔒 Client Secret: {application.client_secret}")

if __name__ == '__main__':
    create_oauth_application()