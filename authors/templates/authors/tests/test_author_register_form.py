from unittest import TestCase  # type: ignore # noqa: F401
from authors.forms import RegisterForm
from parameterized import parameterized  # type: ignore # noqa: F401


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),

    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('email', 'The e-mail must be valid.'),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.')

    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current_placeholder = form[field].field.help_text
        self.assertEqual(current_placeholder, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
        ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current_placeholder = form[field].field.label
        self.assertEqual(current_placeholder, needed)
