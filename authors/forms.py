from django import forms  # type: ignore # noqa: F401
from django.contrib.auth.models import User  # type: ignore # noqa: F401


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
