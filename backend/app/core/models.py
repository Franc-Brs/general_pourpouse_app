"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user. Extra fileds useful when adding a name
        for example"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self. create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # field we want to use for auth
    USERNAME_FIELD = 'email'


class Chiamate(models.Model):
    """List of the reconcile-check-post calls to third-party services."""

    datetime_creation = models.DateTimeField(auto_now_add=True,)
    # requires=IS_NOT_EMPTY(), default=now, update=now, writable=False
    datetime = models.DateTimeField(auto_now=True,)
    chiamata = models.TextField(blank=True)
    status = models.CharField(max_length=255)  # writable=False
    # requires=IS_IN_SET([IP_TEST,IP_PROD])
    server = models.CharField(max_length=255)
    risposta_server_terzo = models.TextField(blank=True)  # writable=False

    def __str__(self):
        return self.chiamata
