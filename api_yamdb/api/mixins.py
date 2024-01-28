from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class ModelMixinSet(
    CreateModelMixin, DestroyModelMixin,
    ListModelMixin, GenericViewSet
):
    """Миксин для моделей Category, Genre и Title."""

    pass
