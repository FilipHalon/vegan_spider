from django import forms
from django.core.exceptions import ValidationError

from vegan_spider_app.models import User


class NewUserCreateForm(forms.ModelForm):
    password_confirm = forms.CharField(max_length=128, widget=forms.PasswordInput, label="Potwierdź hasło")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        widgets = {'password': forms.PasswordInput}

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise ValidationError("Hasła muszą być takie same.")
