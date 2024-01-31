from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка на корректность года выхода произведения."""

    now = timezone.now().year
    if value <= 0 or value > now:
        raise ValidationError(
            f'{value} должен быть меньше или равен {now}!'
        )
    return value
