from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    # Tornamos o campo de e-mail obrigatório no registo
    email = forms.EmailField(required=True, label="E-mail")

    class Meta:
        model = User
        fields = ('username', 'email') # Inclui o username e o email (as passwords vêm por defeito no UserCreationForm)

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data['email']
        if commit:
            usuario.save()
        return usuario