from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class NewUserCreateForm(forms.ModelForm):
    password_confirm = forms.CharField(max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        widgets = {'password': forms.PasswordInput}

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise ValidationError("Hasła muszą być takie same.")
