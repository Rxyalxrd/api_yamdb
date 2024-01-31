from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SendEmailConfirmation,
    SendToken,
    TitleViewSet,
    UserViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    'users',
    UserViewSet,
    basename='users',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='сategories',
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles',
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres',
)

auth_urls = [
    path('token/', SendToken.as_view()),
    path('signup/', SendEmailConfirmation.as_view()),
]
urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
