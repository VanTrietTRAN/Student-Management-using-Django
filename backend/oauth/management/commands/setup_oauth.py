from django.core.management.base import BaseCommand
from oauth.models.oauth2 import Application
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create and show OAuth2 application details'

    def handle(self, *args, **kwargs):
        # Get admin user
        admin_user = User.objects.get(email='admin@university.edu')
        
        # Delete existing application if it exists
        Application.objects.filter(name='Default Application').delete()
        
        # Create application
        application = Application.objects.create(
            name='Default Application',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=admin_user,
            type=Application.APPLICATION_TYPE_SYSTEM
        )
        
        self.stdout.write('Created OAuth2 Application:')
        self.stdout.write(f'Client ID: {application.client_id}')
        self.stdout.write(f'Client Secret: {application.client_secret}')