from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    date_joined = models.DateTimeField(default=timezone.now)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
