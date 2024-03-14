from django.shortcuts import render, redirect  # type: ignore # noqa: F401
from .forms import RegisterForm  # type: ignore # noqa: F401
from django.http import Http404  # type: ignore # noqa: F401
from django.contrib import messages  # type: ignore # noqa: F401
from django.urls import reverse  # type: ignore # noqa: F401


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)  # noqa: F841

    if form.is_valid():
        # aqui se o form for valido eu não vou salvar a senha do usuario
        # na base de dados, por isso o commit=False
        user = form.save(commit=False)
        # e aqui a password vai ficar salva no banco de dados, mas
        # vai estar criptografada.
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')

        del (request.session['register_form_data'])

    return redirect('authors:register')


def login_view(request):
    return render(request, 'authors/pages/login.html')


def login_create(request):
    return render(request, 'authors/pages/login.html')
