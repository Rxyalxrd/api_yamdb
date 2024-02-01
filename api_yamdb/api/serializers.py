from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from reviews.models import (
    Category,
    Comment,
    EmailConfirmation,
    Genre,
    Review,
    Title,
    User,
)

from .utils import generate_user_confirmation_code


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы c пользователями."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        lookup_field = ('username',)

    def validate_username(self, value):
        """Валидация имени пользователя."""

        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве username!'
            )
        return value

    def update(self, instance, validated_data):
        """Обновление роли только администратором или суперпользователем."""
        user = self.context['request'].user
        if (
            'role' in validated_data
            and not user.is_admin
            and not user.is_superuser
        ):
            validated_data.pop('role')
        return super().update(instance, validated_data)


class SendEmailSerializer(serializers.ModelSerializer):
    """Сериализатор для отправки кода подтверждения на почту."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        """Валидация имени пользователя."""

        if value == 'me':
            raise serializers.ValidationError('Имя "me" не разрешено!')
        return value

    def create(self, validated_data):
        """Создать пользователя и присвоить ему код подтверждения."""

        user = User.objects.create(**validated_data)
        user.user_confirmation_code = generate_user_confirmation_code()
        user.save()
        return user


class EmailConfirmationSerializer(serializers.ModelSerializer):
    """Сериализатор для проверки кода подтверждения пользователя."""

    username = serializers.CharField()

    class Meta:
        model = EmailConfirmation
        fields = (
            'username',
            'confirmation_code',
        )

    def validate(self, data):
        """Валидация кода подтверждения."""

        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user.user_confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения!')
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    """Серилизатор для создания произведения."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    year = serializers.IntegerField(required=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'description', 'genre', 'id')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return TitleReadSerializer(instance, context=context).data

    def validate_year(self, value):
        now = timezone.now().year
        if value <= 0 or value > now:
            raise serializers.ValidationError(
                f'{value} должен быть меньше или равен {now}!'
            )
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    """Серилизатор для прочтения произведения."""

    genre = GenreSerializer(
        many=True,
    )
    category = CategorySerializer()
    rating = serializers.FloatField(default=0.0)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        """Проверяет валидность данных перед сохранением."""

        request = self.context.get('request')

        if request.method != 'POST':
            return data

        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)

        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Может существовать только один отзыв!')

        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
