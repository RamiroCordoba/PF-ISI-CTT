from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    password2 = forms.CharField(
        label="Repetir Contraseña", widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]