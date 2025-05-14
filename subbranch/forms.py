# subbranch/forms.py

from django import forms
from .models import Subbranch
from .models import BankAccount
from store.models import Product
class SubBranchImageForm(forms.ModelForm):
    class Meta:
        model = Subbranch
        fields = ['image']

class SubbranchLoginForm(forms.Form):
    username = forms.CharField()
    store_name = forms.CharField()
    subbranch_id = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = [
            'account_type', 'bank_name', 'account_number', 'account_name',
            'bank_code', 'stripe_id', 'paypal_address'
        ]
        widgets = {
            'account_number': forms.TextInput(attrs={'placeholder': 'Enter Account Number'}),
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'regular_price', 'stock', 'unit', 'image', 'description']