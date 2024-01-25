from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, url_path='me', methods=['GET', 'PATCH'])
    def self_information(self, request, pk=None):
        """
        Возвращает данные о пользователе сделавшего GET-запрос.
        Вносит изменения в данные учетной записи пользователя 
        сделавшего PATCH-запрос.
        """
        serializer = self.get_serializer(request.user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data)
