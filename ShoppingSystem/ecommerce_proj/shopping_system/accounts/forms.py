from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from accounts.models import CustomUser  # Import your custom user model
from django import forms
from .models import Product

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    
    class Meta:
        model = CustomUser  # Use your custom user model
        fields = ('username', 'email', 'password1', 'password2')

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'rate']
