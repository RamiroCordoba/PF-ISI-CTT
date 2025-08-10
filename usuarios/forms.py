from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado
from django.contrib.auth.models import Group

class UsuarioEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Roles",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "grupos"
        ]

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Roles",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "grupos"
        ]
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)