from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import UserSerializer
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdminUser,
    ]
    filter_backends = filters.SearchFilter
    search_fields = ('username',)