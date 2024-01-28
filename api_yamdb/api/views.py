from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter

from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    AdminModeratorAuthorOrReadOnly,
    IsModerator,
    IsAuthorOrReadOnly,
)
from .serializers import (
    EmailConfirmationSerializer,
    SendEmailSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleCreateSerializer,
    CommentSerializer,
    ReviewSerializer,
)
from .utils import (
    generate_user_confirmation_code,
    send_mail_with_confirmation_code,
)
from reviews.models import User, Category, Genre, Title, Review


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        url_path='me',
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
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
            if serializer.is_valid() and 'role' not in request.data:
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
                return Response(
                    {"email": "Неверный адрес электронной почты!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.user_confirmation_code = generate_user_confirmation_code()
            user.save()
            send_mail_with_confirmation_code(user)
            return Response(request.data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(
                User, username=serializer.validated_data['username']
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
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'patch', 'delete']


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'patch', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (
        AdminModeratorAuthorOrReadOnly,
    )  # AdminModeratorAuthorPermission
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = (
        AdminModeratorAuthorOrReadOnly,
    )  # AdminModeratorAuthorPermissionIsAdmin,IsModerator,IsAuthorOrReadOnly
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
