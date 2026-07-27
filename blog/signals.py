from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AuthorProfile


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        AuthorProfile.objects.create(user=instance)
    else:
        # Save profile if it exists, or create it if missing
        AuthorProfile.objects.get_or_create(user=instance)
