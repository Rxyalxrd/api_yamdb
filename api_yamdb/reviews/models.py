from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username

ROLE = (
    ('admin', 'админ'),
    ('moderator', 'модератор'),
    ('user', 'пользователь'),
)


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        validators=[username_validator, validate_username],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, choices=ROLE, default='user')
