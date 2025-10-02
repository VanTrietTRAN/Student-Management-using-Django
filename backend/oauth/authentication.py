from rest_framework.authentication import BaseAuthentication


class MiddlewareAuthAuthentication(BaseAuthentication):
    """Authentication class that returns the user and token already attached
    to the HttpRequest by OAuthHeaderMiddleware.

    This lets DRF treat our middleware-attached AccessToken as the authentication
    result so permissions like IsAuthenticated and TokenHasActionScope work.
    """

    def authenticate(self, request):
        # Avoid touching request.auth (DRF's property) to prevent recursion.
        # The middleware attaches the token to the underlying Django HttpRequest
        # so read it from request._request which is the original HttpRequest.
        django_req = getattr(request, '_request', None) or request
        token = getattr(django_req, 'auth', None)
        if token is None:
            return None
        user = getattr(token, 'user', None)
        if user is None:
            return None
        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer'
