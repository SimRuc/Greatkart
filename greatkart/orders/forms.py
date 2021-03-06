from dataclasses import fields
from pyexpat import model
from socket import fromshare
from django import forms
from .models import Payment, Order, OrderProduct


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']
