from django.template.defaultfilters import default
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_administrator = models.BooleanField(default=False)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, default="John Doe")
    def __str__(self):
        return self.username