from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser, PermissionsMixin):
    is_verified = models.BooleanField(default=False, null=False)
    picture = models.URLField(null=True, blank=True)
    banner = models.URLField(null=True, blank=True)
    birth_date = models.DateField(null=True)

    REQUIRED_FIELDS = (
        "first_name",
        "last_name",
        "email",
    )


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follow = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="followers",
    )
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "follow",
        )


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    content = models.TextField(blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
