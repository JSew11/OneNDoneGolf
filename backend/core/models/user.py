from typing import Any
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE

class UserManager(BaseUserManager):
    """Manager for user models.
    """
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('No email provided - this field is required.')
        if not username:
            raise ValueError('No username provided - this field is required.')
        if not password:
            raise ValueError('No password provided - this field is required.')
        email = self.normalize_email(email)
        user: User = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create(self, **kwargs: Any) -> Any:
        """Create and save a regular User with the given credentials."""
        username = kwargs.pop('username', None)
        email = kwargs.pop('email', None)
        password = kwargs.pop('password', None)
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(username=username, email=email, password=password, **kwargs)

    def create_superuser(self, username, email, password, **extra_fields):
        """Create and save a SuperUser with the given credentials."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)
    
class User(AbstractUser, SafeDeleteModel):
    """Custom User model for full control over different fields, and to allow for
    soft deletion.
    """
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE_CASCADE
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    objects = UserManager()

    class Meta:
        ordering = ['created']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    # database info
    id = models.BigAutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # user info
    username = models.CharField(unique=True, max_length=25)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
