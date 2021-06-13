from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=200)


class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)


class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    date_joined = models.DateTimeField(default=timezone.now)
    # nullable, null if deleted foreign row
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    username = None

    # we will use the username field as email (so they are treated as one)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
