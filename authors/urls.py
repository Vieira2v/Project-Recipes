from django.urls import path  # type: ignore # noqa: F401
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
]
