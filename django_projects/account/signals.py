from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from account.models import ProfileInfo


@receiver(post_save, sender=ProfileInfo)
def send_signup_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Sleek Boutique!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.user.email]

        html_message = render_to_string('email_templates/signup_email.html', {
            'user': instance,
        })

        send_mail(subject, None, from_email, recipient_list, html_message=html_message)
