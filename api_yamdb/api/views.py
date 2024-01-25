from rest_framework import filters
from rest_framework import viewsets

from .serializers import UserSerializer
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = filters.SearchFilter
    search_fields = ('username',)
