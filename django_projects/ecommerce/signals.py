from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from ecommerce.models import OrderedItem


@receiver(post_save, sender=OrderedItem)
def send_order_confirmation(sender, instance, created, **kwargs):
    if created:
        target_order_id = instance.order.order_id
        ordered_items = OrderedItem.objects.filter(order__order_id=target_order_id)

        cart_items_data = []
        total_price = 0

        for item in ordered_items:
            cart_items_data.append(
                {
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                }
            )
            total_price += item.product.price * item.quantity
            item.delete()

        subject = 'Sleek Boutique -- Order Confirmation'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.order.user.email]

        context = {
            'order': instance.order,
            'total_price': total_price,
            'cart_items_data': cart_items_data
        }

        html_message = render_to_string('email_templates/order_confirmation.html', context)
        message = 'Thank you for placing an order with us!'

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
