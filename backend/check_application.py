from oauth2_provider.models import Application

def get_application_details():
    app = Application.objects.get(name='Default Application')
    print(f'Client ID: {app.client_id}')
    print(f'Client Secret: {app.client_secret}')