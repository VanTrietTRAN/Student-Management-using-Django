from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

def create_or_update_application(ApplicationModel, client_id, client_secret, name='Client'):
    if not client_id:
        return None
    app, created = ApplicationModel.objects.get_or_create(client_id=client_id)
    app.name = name
    # store secret if provided (ClientSecretField will hash on save)
    if client_secret:
        app.client_secret = client_secret
    # allow all scopes by default so local/dev can request any scope
    app.scope = '__all__'
    # set authorization grant type to password for resource owner flow
    app.authorization_grant_type = 'password'
    # mark type as client (matches project conventions)
    try:
        # some Application model variants have 'type' field
        app.type = getattr(app, 'type', 'client') or 'client'
    except Exception:
        pass
    app.save()
    return app


class Command(BaseCommand):
    help = 'Create or update OAuth client applications from settings (BUSINESS/ECOMMERCE)'

    def handle(self, *args, **options):
        from oauth.models.oauth2 import Application

        business_id = getattr(settings, 'BUSINESS_CLIENT_ID', None)
        business_secret = getattr(settings, 'BUSINESS_CLIENT_SECRET', None)
        ecom_id = getattr(settings, 'ECOMMERCE_CLIENT_ID', None)
        ecom_secret = getattr(settings, 'ECOMMERCE_CLIENT_SECRET', None)

        apps = []
        b = create_or_update_application(Application, business_id, business_secret, name='Business Client')
        if b is not None:
            apps.append(('business', b.client_id))
        e = create_or_update_application(Application, ecom_id, ecom_secret, name='Ecommerce Client')
        if e is not None:
            apps.append(('ecommerce', e.client_id))

        self.stdout.write(self.style.SUCCESS(f'Initialized OAuth applications: {apps}'))
