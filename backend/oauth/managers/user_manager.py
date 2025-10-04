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
        role_ids=[]
    ):
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)

        if password is None:
            raise ValueError("User must have a password")

        user = self.model(email=email, first_name=first_name or '', last_name=last_name or '')
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.set_password(password)
        user.active = active
        user.save(using=self._db)

        if role_ids is not None and len(role_ids) > 0:
            role_ids = [UUID(hex=item) if isinstance(item, str) else item for item in role_ids]
            user.roles.add(*role_ids)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('active', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, first_name=extra_fields.get('first_name'), last_name=extra_fields.get('last_name'), is_superuser=True, is_staff=True, active=extra_fields.get('active', True))
