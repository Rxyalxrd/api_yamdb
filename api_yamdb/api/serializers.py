from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
