from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re
from rest_framework.reverse import reverse

class CustomUserManager(BaseUserManager):
    """
    Custom manager for handling user creation with email as the unique identifier.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields for the user model.

        Raises:
            ValueError: If the email or password is not provided.

        Returns:
            CustomUser: The created user instance.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        if not password:
            raise ValueError(_("Password cannot be empty"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given email and password.

        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for the superuser model.

        Raises:
            ValueError: If `is_staff` or `is_superuser` is not set to True.

        Returns:
            CustomUser: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Custom user model where email is the unique identifier instead of username.
    """

    username = models.CharField(
        blank=True,
        null=True,
        max_length=10
    )
    email = models.EmailField(
        _("Email Address"),
        unique=True,
        max_length=200
    )
    bio = models.CharField(
        _("Tell Us About Yourself"),
        max_length=500,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def validate_email(self):
        """
        Validates the email format against a regex pattern.

        Raises:
            ValidationError: If the email format is invalid.
        """
        re_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(re_pattern, self.email):
            raise ValidationError(_(f"{self.email} is not a valid email address."))

    def normalize_email(self):
        """
        Normalizes the email to lowercase.
        """
        self.email = self.email.lower()

    def normalize_bio(self):
        """
        Normalizes the bio to lowercase.
        """
        self.bio = self.bio.lower()

    def save(self, *args, **kwargs):
        """
        Overridden save method to ensure email and bio are normalized and validated.
        """
        self.normalize_email()
        self.validate_email()
        self.normalize_bio()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Retrieves user specific detail page.
        """
        return reverse('users-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['email']

class LibraryProfile(models.Model):
    """
    Model for storing additional information about library users.
    """

    class Roles(models.TextChoices):
        MEMBER = 'Member', _('Member')
        LIBRARIAN = 'Librarian', _('Librarian')

    role = models.CharField(
        _("User Assigned Role at Library"),
        choices=Roles.choices,
        max_length=20
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    member_since = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.role}, joined on {self.member_since}"
