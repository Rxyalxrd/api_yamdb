from random import randint

from django.core.mail import send_mail


def generate_user_confirmation_code():
    """Сгенерировать код подтверждения."""

    return str(randint(10000, 99999))


def send_mail_with_confirmation_code(user):
    """Отправить письмо на почту с кодом подтверждения."""

    send_mail(
        subject='Код потверждения',
        message=f'Ваш код подтверждения - {user.user_confirmation_code}',
        from_email='test_backend@yambd.not',
        recipient_list=[f'{user.email}'],
        fail_silently=True,
    )
