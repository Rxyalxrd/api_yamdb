from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from api_yamdb.const import (
    LEN_FOR_CONF_CODE,
    LEN_FOR_SLUG,
    LEN_FOR_NAME,
)
from .validators import validate_year
from .user import User


class EmailConfirmation(models.Model):
    """Модель для подтверждения учетной записи."""

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=LEN_FOR_CONF_CODE,
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
        unique=True, verbose_name='Название категории', max_length=LEN_FOR_NAME
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
        db_index=True,
        max_length=LEN_FOR_SLUG,
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
        max_length=LEN_FOR_NAME,
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        db_index=True,
        max_length=LEN_FOR_SLUG,
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
        max_length=LEN_FOR_NAME,
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
        on_delete=models.SET_DEFAULT,
        related_name='titles',
        verbose_name='Категория',
        default='Категория не определена.',
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
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
        null=False,
        verbose_name='Текст отзыва.',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва.',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Значение должно быть не менее 1.'),
            MaxValueValidator(10, message='Значение должно быть не более 10.'),
        ],
        verbose_name='Оценка от 1 до 10.',
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
        verbose_name='Текст комментария.',
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
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
