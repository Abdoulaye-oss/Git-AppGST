from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()
class UserForm(UserCreationForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé utilisant AuthenticationForm de Django.
    """
    username = forms.CharField(label="Nom d'utilisateur", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(label="Mot de passe", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))
