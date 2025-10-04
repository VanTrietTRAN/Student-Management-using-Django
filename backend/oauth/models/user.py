import uuid

from django.utils import timezone
from ..managers import UserManager
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Giảng viên'),
        ('student', 'Sinh viên'),
        ('training_staff', 'Nhân viên phòng đào tạo'),
        ('student_affairs', 'Nhân viên phòng công tác sinh viên'),
    ]
    
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    password = models.CharField(verbose_name="password", max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='student',
        verbose_name="Loại người dùng"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name="Ảnh đại diện"
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    active = models.BooleanField(default=True)
    roles = models.ManyToManyField(
        'Role',
        blank=True,
        verbose_name="Vai trò"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"  # username
    
    # Use custom manager that implements create_user and create_superuser
    objects = UserManager()

    class Meta:
        db_table = "oauth_users"
        app_label = 'oauth'

    def __str__(self):
        return str(self.id)

    @property
    def is_active(self):
        return self.active