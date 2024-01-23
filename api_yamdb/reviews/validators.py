from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверка на корректность имени пользователя"""

    if value.lower() == 'me':
        raise ValidationError(
            'Выберите другое имя пользователя'
        )