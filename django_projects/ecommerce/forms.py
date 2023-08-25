from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator


class CheckoutForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('easypaisa', 'EasyPaisa'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery', 'Cash on Delivery')
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect)
    shipping_address = forms.CharField(max_length=500)
    contact_info = forms.CharField(
        max_length=11,
        validators=[MinLengthValidator(11), MaxLengthValidator(11)],
        help_text="Please enter your 11-digit contact number."
    )
