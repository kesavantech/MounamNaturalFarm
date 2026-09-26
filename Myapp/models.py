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

class Website(models.Model):
    id = models.PositiveSmallIntegerField(
        primary_key=True, default=1, editable=False
    ) 
# primary_key=True  # Unique ID | default=1         # Always ID 1 | editable=False    # Cannot edit in Admin
    logo = models.ImageField(upload_to="logo")
    logo_radius = models.PositiveIntegerField(default=60)
    heading = models.CharField(max_length=100)
    sub_heading = models.CharField(max_length=100)
    text_color = models.CharField(max_length=30, default="#000000")
    font_size  = models.PositiveIntegerField(default=16)
    bg_color = models.CharField( max_length=20, default="#ffffff" )
    description = models.TextField(blank=True, default="")

    def __str__(self): 
        return self.heading
    

class HomePage(models.Model):
    main_image = models.ImageField(
        upload_to="home/"
    )
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    bullet_point_1 = models.CharField(max_length=100)
    bullet_point_2 = models.CharField(max_length=100)
    bullet_point_3 = models.CharField(max_length=100)

    def __str__(self):
        return self.title