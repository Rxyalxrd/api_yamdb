from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Категории."""

    name = models.CharField(
        verbose_name='Название категории',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры."""

    name = models.CharField(
        verbose_name='Название жанра',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год создания',
        null=True,
        help_text='Год выхода',
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
