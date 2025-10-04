import logging
from django.conf import settings
from oauth2_provider.contrib.rest_framework.permissions import TokenMatchesOASRequirements


log = logging.getLogger("oauth2_provider")


class TokenHasActionScope(TokenMatchesOASRequirements):
    """
    :attr:alternate_required_scopes: dict keyed by view action name with value: iterable alternate scope lists.
    For each method, a list of lists of allowed scopes is tried in order and the first to match succeeds.

    @example
    required_alternate_scopes = {
       'get': [['read']],
       'update': [['create1','scope2'], ['alt-scope3'], ['alt-scope4','alt-scope5']],
    }

    TODO: DRY: subclass TokenHasScope and iterate over values of required_scope?
    """

    def has_permission(self, request, view):
        token = request.auth

        if not token:
            return False

        if hasattr(token, "scope"):  # OAuth 2
            required_alternate_scopes = self.get_required_alternate_scopes(request, view)

            a = view.action.lower() if view.action is not None else None

            if a in required_alternate_scopes:
                log.debug(
                    "Required scopes alternatives to access resource: {0}".format(
                        required_alternate_scopes[a]
                    )
                )
                for alt in required_alternate_scopes[a]:
                    if token.is_valid(alt):
                        return True
                return False
            else:
                log.warning("no scope alternates defined for method {0}".format(a))
                return False

        assert False, (
            "TokenHasActionScope requires the"
            "`oauth.rest_framework.OAuth2Authentication` authentication "
            "class to be used."
        )

class IsAdministrator(TokenMatchesOASRequirements):
    """
    Allows access only to administrator.
    """

    def has_permission(self, request, view):
        token = request.auth
        if token is not None and token.application is not None and token.application.id == settings.BUSINESS_CLIENT_ID:
            return True
        return False


class IsOwnerOrHasActionScope(object):
    """
    Allows access to object when the token belongs to the resource owner
    or when the token has one of the required_alternate_scopes for the view action.

    This permission is intended to be used together with TokenHasActionScope
    in viewsets. has_permission returns True (so it doesn't block top-level
    checks) while has_object_permission enforces owner-or-scope checks.
    """

    def has_permission(self, request, view):
        # Do not block initial permission checks; rely on TokenHasActionScope
        return True

    def has_object_permission(self, request, view, obj):
        token = request.auth
        if token is None:
            return False

        # First allow if token satisfies required scopes for the action
        action = view.action.lower() if getattr(view, 'action', None) else None
        required = getattr(view, 'required_alternate_scopes', {})
        if action in required:
            for alt in required[action]:
                if token.is_valid(alt):
                    return True

        # Next, try owner check. The view may define `owner_field` to indicate
        # which attribute on the object references the owner (e.g., 'student' or 'user').
        owner_field = getattr(view, 'owner_field', None)
        if owner_field and hasattr(obj, owner_field):
            owner = getattr(obj, owner_field)
            owner_id = getattr(owner, 'id', getattr(owner, 'pk', owner))
            return str(owner_id) == str(token.user.id)

        # Generic fallbacks for common owner attributes
        for f in ('student', 'user', 'owner'):
            if hasattr(obj, f):
                owner = getattr(obj, f)
                owner_id = getattr(owner, 'id', getattr(owner, 'pk', owner))
                return str(owner_id) == str(token.user.id)

        return False