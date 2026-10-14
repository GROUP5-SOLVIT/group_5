from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True)
    role = models.ForeignKey(
        'roles.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.email:
            self.email = UserManager.normalize_email(self.email.strip()).lower()
        super().save(*args, **kwargs)

    def get_all_permissions(self):
        perms = set(super().get_all_permissions())
        if self.role:
            perms.update(self.role.get_all_permissions())
        return perms

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return perm in self.get_all_permissions()
