from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault("role", "ADMIN")

        return super().create_superuser(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    location = models.CharField(max_length=150, blank=True)
    address = models.TextField(blank=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username