from oauth2_provider.models import Application
from django.contrib.auth import get_user_model

User = get_user_model()

def create_oauth_app():
    # Get admin user
    admin_user = User.objects.get(email='admin@university.edu')
    
    # Delete existing application if it exists
    Application.objects.filter(name='Default Application').delete()
    
    # Create application
    application = Application.objects.create(
        name='Default Application',
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
        user=admin_user
    )
    
    print('Created OAuth2 Application:')
    print(f'Client ID: {application.client_id}')
    print(f'Client Secret: {application.client_secret}')

if __name__ == '__main__':
    create_oauth_app()