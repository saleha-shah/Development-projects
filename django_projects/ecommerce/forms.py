from django import forms


class CheckoutForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('easypaisa', 'EasyPaisa'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery', 'Cash on Delivery')
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect)
    shipping_address = forms.CharField(max_length=500)
    contact_info = forms.CharField(max_length=11)
