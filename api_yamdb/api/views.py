from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import (
    AdminModeratorAuthorOrReadOnly,
    IsAdmin,
    IsAdminOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    EmailConfirmationSerializer,
    GenreSerializer,
    ReviewSerializer,
    SendEmailSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
    UserSerializer,
)
from .utils import (
    generate_user_confirmation_code,
    send_mail_with_confirmation_code,
)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        url_path='me',
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
    )
    def self_information(self, request, pk=None):
        """
        Возвращает данные о пользователе сделавшего GET-запрос.
        Вносит изменения в данные учетной записи пользователя
        сделавшего PATCH-запрос.
        """

        serializer = self.get_serializer(request.user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data)


class SendEmailConfirmation(APIView):
    """Вьюсет для отправки кода подтверждения на почту."""

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        Создать пользователя в БД и отправить на почту
        код подтверждения учетной записи.
        """

        serializer = SendEmailSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        if username in User.objects.values_list('username', flat=True):
            user = get_object_or_404(User, username=username)
            if user.email != email:
                if not serializer.is_valid():
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            user.user_confirmation_code = generate_user_confirmation_code()
            user.save()
            send_mail_with_confirmation_code(user)
            return Response(request.data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(
                User, username=serializer.validated_data.get('username')
            )
            send_mail_with_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendToken(APIView):
    """
    Вьюсет для отправки токена авторизации
    если пользователь ввел правильный username и confirmation_code.
    """

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """Получить токен авторизации."""
        serializer = EmailConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(ModelMixinSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ModelMixinSet):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """Возвращает класс сериализатора в зависимости от действия."""

        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        """Получает объект класса Review."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'), title=title
        )

    def get_queryset(self):
        """Получает и возвращает список комментариев для конкретного отзыва."""

        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Создает новый комментарий для отзыва."""

        author = self.request.user
        review = self.get_review()
        serializer.save(author=author, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination

    def get_title(self):
        """Получает объект класса Title."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Получает и возвращает список отзывов для конкретного заголовка."""

        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создает новый отзыв или обновляет существующий."""

        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        author = self.request.user
        existing_review = Review.objects.filter(
            title=title, author=author
        ).first()
        if existing_review:
            serializer.update(existing_review, serializer.validated_data)
        else:
            serializer.save(author=author, title=title)
