from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка на корректность года выхода произведения."""

    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{now} должен быть меньше или равен {value}!'
        )
