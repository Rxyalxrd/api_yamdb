from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from reviews.models import Category, Genre, Title
from api.filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleCreateSerializer)


class CategoryViewSet(ModelMixinSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ModelMixinSet):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelMixinSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer
