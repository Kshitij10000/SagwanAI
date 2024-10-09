# PaperTrade/forms.py
from django import forms
from .models import Order, Ticker

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ticker', 'order_type', 'quantity']
        widgets = {
            'ticker': forms.Select(attrs={'class': 'form-control'}),
            'order_type': forms.Select(choices=Order.ORDER_TYPES, attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
