from django.shortcuts import render, redirect  # type: ignore # noqa: F401
from .forms import RegisterForm
from django.http import Http404  # type: ignore # noqa: F401


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)  # noqa F841
    form = RegisterForm()
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)  # noqa F841

    return redirect('authors:register')
