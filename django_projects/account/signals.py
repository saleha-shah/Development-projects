from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from account.models import ProfileInfo
from ecommerce.models import OrderedItem


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


@receiver(post_save, sender=OrderedItem)
def send_order_confirmation(sender, instance, created, **kwargs):
    if created:
        selected_cart_item = instance.cart_item
        selected_cart_items = [selected_cart_item]
        subject = 'Sleek Boutique--Order Confirmation'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.order.user.email]

        context = {
            'order': instance.order,
            'cart_items': selected_cart_items,
        }

        html_message = render_to_string('email_templates/order_confirmation.html', context)
        message = 'Thank you for placing an order with us!'

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
