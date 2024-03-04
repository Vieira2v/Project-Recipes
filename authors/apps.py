from django.apps import AppConfig  # type: ignore # noqa: F401


class AuthorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authors"
