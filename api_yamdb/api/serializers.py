from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .utils import generate_user_confirmation_code
from reviews.models import (
    Category,
    Genre,
    Title,
    Comment,
    Review,
    EmailConfirmation,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""

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

    def validate_username(self, value):
        """Валидация имени пользователя."""
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве username!'
            )
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if 'role' in validated_data and user.role != 'admin':
            validated_data.pop('role')
        return super().update(instance, validated_data)


class SendEmailSerializer(serializers.ModelSerializer):
    """Сериализатор для отправки кода подтверждения на почту."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        """Валидация имени пользователя."""
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве username!'
            )
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
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        """Валидация кода подтверждения."""
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.user_confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения!')
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        model = Genre
        exclude = ('id',)


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

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """Серилизатор для прочтения произведения."""

    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    title = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        model = Review
        fields = '__all__'
