from django.shortcuts import render  # type: ignore # noqa: F401
from .forms import RegisterForm


def register_view(request):
    form = RegisterForm()
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })
