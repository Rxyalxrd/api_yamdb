from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (
    ('admin', 'администратор'),
    ('moderator', 'модератор'),
    ('user', 'пользователь'),
)


class User(AbstractUser):
    """Кастомная модель позователя."""

    bio = models.TextField(
        'О себе',
        blank=True,
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
    )
    role = models.CharField(
        'Роль',
        max_length=15,
        choices=ROLE,
        default='user',
    )
    user_confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=5,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
