from django import forms  # type: ignore # noqa: F401
from django.contrib.auth.models import User  # type: ignore # noqa: F401


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex: Vin')
        add_placeholder(self.fields['last_name'], 'Ex: Diesel')
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'The e-mail must be valid'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }
        widgets = {
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }