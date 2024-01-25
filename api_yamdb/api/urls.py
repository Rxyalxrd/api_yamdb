from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet

auth_urls = [
    path('token/', TokenObtainPairView.as_view()),
    path('signup/', UserViewSet.as_view({'post': 'create'})),
]
urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include('djoser.urls')),
]
