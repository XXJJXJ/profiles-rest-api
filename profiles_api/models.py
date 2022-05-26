from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Part 2
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, password=None): # means pw is default to None if not specified
        """Creates a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password) #method inherited from AbstractBaseUser, hashes the password
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and save a new superuser with given details"""
        user = self.create_user(email, name, password) #note, self is automatically passed in in python

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


# In Python, class declarations need to be 2 lines spacing apart

# Part 1
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager() # to be created in the future

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email
