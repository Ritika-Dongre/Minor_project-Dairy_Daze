from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

USER_TYPE = (
    ("Subbranch", "Subbranch"),
    ("Customer", "Customer"),
)


from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    




# AbtractUser is a base class, provides customizable user models for us.
class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True)

    # using email for login purposes.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    # save instance of a model to the database, insert or updates the records.
    def save(self, *args, **kwargs):
        email_username, _ = self.email.split("@")
        # name@gmail.com -> email_username=name, _=gmail.com
        if not self.username:
            self.username = email_username
        super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", default="default-user.jpg", null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    user_Type = models.CharField(max_length=20, choices=USER_TYPE, default="Customer")
    state = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    zipcode = models.CharField(max_length=10, default="")
    def __str__(self):
        return f"{self.full_name}'s Profile"

    def save(self, *args, **kwargs):
        """Auto-populate fields if empty"""
        if not self.full_name and self.user:
            self.full_name = self.user.username
        if not self.mobile:
            self.mobile = "0000000000"  # Generic default
        super().save(*args, **kwargs)