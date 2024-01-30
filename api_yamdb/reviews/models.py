from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator
)
from django.db import models

from .validators import validate_year


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
        unique=True
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

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class EmailConfirmation(models.Model):
    """Модель для подтверждения учетной записи."""

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=5,
        unique=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='confirmations',
    )


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        unique=True,
        verbose_name='Название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
        db_index=True,
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Слаг категории содержит недопустимый символ',
            )
        ],
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанров."""

    name = models.CharField(
        unique=True,
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        db_index=True,
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Слаг жанра содержит недопустимый символ',
            )
        ],
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель Произведений."""

    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200,
        db_index=True,
    )
    year = models.IntegerField(
        verbose_name='Год создания',
        default=0,
        help_text='Год создания',
        validators=[validate_year],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория',
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=255,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
    )
    text = models.TextField(
        max_length=1024,
        null=False,
        verbose_name="Текст отзыва.",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name='Автор отзыва.',
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name="Оценка от 1 до 10.",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации.',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author',
            )
        ]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв.',
    )
    text = models.TextField(
        max_length=1024,
        verbose_name="Текст комментария.",
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Автор комментария.',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации.',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        constraints = [
            models.UniqueConstraint(
                fields=['review', 'author'],
                name='unique_review_author',
            )
        ]

    def __str__(self):
        return self.text
