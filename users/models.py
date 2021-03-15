from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core import validators
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        if not username:
            raise ValueError('username must be set')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):

        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(primary_key=True, max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(validators=[validators.EmailValidator], unique=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse('user_room', args=[str(self.username)])

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

