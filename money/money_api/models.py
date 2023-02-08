from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, last_name, first_name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, last_name=last_name, first_name=first_name)

        user.set_password(password)

        user.save(using=self._db) # for support multiply databases in future

        return user

    def create_superuser(self, email, last_name, first_name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, last_name, first_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users"""
    email = models.EmailField(max_length=254, unique=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_stuff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.firstName + self.lastName

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.firstName

    def __str__(self):
        """retrieve string representation of user"""
        return self.email

