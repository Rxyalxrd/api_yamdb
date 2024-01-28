from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SendEmailConfirmation, SendToken, UserViewSet


router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

auth_urls = [
    path('token/', SendToken.as_view()),
    path('signup/', SendEmailConfirmation.as_view()),
]
urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
