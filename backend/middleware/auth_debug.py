import time
from pathlib import Path


class AuthHeaderDebugMiddleware:
    """Simple middleware to log Authorization header and request path to a file for debugging."""

    def __init__(self, get_response):
        self.get_response = get_response
        proj_root = Path(__file__).resolve().parents[1]
        self.log_path = proj_root / 'tmp_requests.log'

    def __call__(self, request):
        try:
            auth = request.META.get('HTTP_AUTHORIZATION') or request.META.get('Authorization')
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} PATH={request.path} AUTH={auth}\n")
        except Exception:
            pass

        return self.get_response(request)
