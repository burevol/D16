from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Response


# TODO добавить заголовок объявления и возможно ссылку на него
@receiver(post_save, sender=Response)
def message_handler(sender, instance, created, *args, **kwargs):
    if created:
        email = instance.recipient.email
        from_user = instance.sender.username
        to_user = instance.recipient.first_name
        text = instance.content
        send_mail(
            f'{to_user}, на ваше объявление откликнулись!',
            text,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
