import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка на корректность года выхода произведения."""

    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{now} должен быть меньше или равен {value}!'
        )


def validate_username(value):
    """Проверка на корректность юзернейма."""

    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )


def username_me(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя "me" не разрешено.'
        )
    return value
