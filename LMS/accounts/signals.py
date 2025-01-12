from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import LibraryProfile, CustomUser
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=CustomUser)
def create_library_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a LibraryProfile instance
    """
    if created:
        role = 'librarian' if instance.is_staff else 'member'
        LibraryProfile.objects.create(user=instance, role=role)


@receiver(post_save, sender=User)
def create_or_ensure_tokens(sender, instance, created, **kwargs):
    """
    Signal to create a token for newly created users or ensure every user has a token.
    """
    if created:
        Token.objects.create(user=instance)
    else:
        # Ensure every user has a token
        users_without_tokens = User.objects.exclude(id__in=Token.objects.values_list('user_id', flat=True))
        for user in users_without_tokens:
            Token.objects.get_or_create(user=user)
