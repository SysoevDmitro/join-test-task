from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_registration_email(user_email, event_title):
    send_mail(
        'Event Registration Confirmation',
        f'You have successfully registered for the event: {event_title}.',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
