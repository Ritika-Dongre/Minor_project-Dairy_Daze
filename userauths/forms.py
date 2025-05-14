from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from django.contrib.auth.password_validation import validate_password
import re

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'form-control',
            'autocomplete': 'name'
        })
    )
    mobile = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your mobile number',
            'class': 'form-control',
            'type': 'tel',
            'pattern': '[0-9]{10,15}'
        })
    )
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your full address',
            'class': 'form-control',
            'rows': 3,
            'style': 'resize: none;'
        })
    )
    state = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your state',
            'class': 'form-control'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your city',
            'class': 'form-control'
        })
    )
    zipcode = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your zipcode',
            'class': 'form-control',
            'pattern': '[0-9]{6}'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control',
            'autocomplete': 'email'
        })
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'mobile', 'address', 'state', 'city', 'zipcode', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update password field widgets
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-control'
        })

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.split()) < 2:
            raise forms.ValidationError("Please enter your full name (first and last name)")
        return full_name

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^[0-9]{10,15}$', mobile):
            raise forms.ValidationError("Please enter a valid 10-15 digit mobile number")
        return mobile

    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode')
        if not re.match(r'^[0-9]{6}$', zipcode):
            raise forms.ValidationError("Please enter a valid 6-digit zipcode")
        return zipcode

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email'].split('@')[0]
        
        if commit:
            user.save()
            # Create the user profile with all fields
            Profile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                mobile=self.cleaned_data['mobile'],
                state=self.cleaned_data['state'],
                city=self.cleaned_data['city'],
                zipcode=self.cleaned_data['zipcode'],
                user_Type="Customer"
            )
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded',
            'placeholder': 'Enter your email'
        }),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded',
            'placeholder': 'Enter your password'
        }),
        required=True
    )