from uuid import UUID
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        email,
        password=None,
        first_name=None,
        last_name=None,
        is_superuser=False,
        is_staff=False,
        active=True,
        role_ids=None,
    ):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        # assign names properly
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.set_password(password)
        user.active = active
        user.save(using=self._db)

        if role_ids:
            role_ids = [UUID(hex=item) if isinstance(item, str) else item for item in role_ids]
            user.roles.add(*role_ids)

        return user
