from pathlib import Path
from django.utils.deprecation import MiddlewareMixin


class OAuthHeaderMiddleware(MiddlewareMixin):
    """Attach AccessToken and user from Authorization: Bearer <token> header.

    This middleware looks up the token in the DB and sets request.auth and
    request.user so DRF views that rely on request.auth will work even if
    the OAuth2Authentication did not populate them (some server setups strip
    the Authorization header before it reaches the framework).
    """

    def process_request(self, request):
        try:
            # Simple file logging for debugging middleware invocation
            try:
                proj_root = Path(__file__).resolve().parents[2]
                log_path = proj_root / 'backend' / 'tmp_oauth_header.log'
                log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(log_path, 'a', encoding='utf-8') as _f:
                    _f.write('middleware invoked\n')
            except Exception:
                pass

            auth = request.META.get('HTTP_AUTHORIZATION') or request.META.get('Authorization')
            try:
                with open(log_path, 'a', encoding='utf-8') as _f:
                    _f.write(f'HTTP_AUTHORIZATION={auth}\n')
            except Exception:
                pass

            if not auth or not isinstance(auth, str):
                return None
            parts = auth.split()
            if len(parts) != 2:
                return None
            scheme, token_str = parts[0].lower(), parts[1]
            if scheme != 'bearer':
                return None

            # Import lazily to avoid import cycles at startup
            from oauth.models.oauth2 import AccessToken

            token_obj = AccessToken.objects.filter(token=token_str).order_by('-id').first()
            try:
                with open(log_path, 'a', encoding='utf-8') as _f:
                    _f.write(f'token_found={bool(token_obj)} token_str_prefix={token_str[:8]}\n')
            except Exception:
                pass

            if token_obj is None:
                return None

            # Ensure token is not expired
            try:
                if getattr(token_obj, 'is_expired', None) and token_obj.is_expired():
                    try:
                        with open(log_path, 'a', encoding='utf-8') as _f:
                            _f.write('token_expired\n')
                    except Exception:
                        pass
                    return None
            except Exception:
                # if any error checking expiration, avoid attaching
                return None

            # Attach token and user
            request.auth = token_obj
            request.user = token_obj.user
            # Remove raw Authorization header to avoid other auth backends re-parsing it
            try:
                if 'HTTP_AUTHORIZATION' in request.META:
                    del request.META['HTTP_AUTHORIZATION']
                if 'Authorization' in request.META:
                    del request.META['Authorization']
                try:
                    with open(log_path, 'a', encoding='utf-8') as _f:
                        _f.write('authorization_header_removed\n')
                except Exception:
                    pass
            except Exception:
                pass
        except Exception:
            # Never raise from middleware in production path
            return None

        return None
