from django.shortcuts import render, redirect  # type: ignore # noqa: F401
from .forms import RegisterForm, LoginForm  # type: ignore # noqa: F401
from django.http import Http404  # type: ignore # noqa: F401
from django.contrib import messages  # type: ignore # noqa: F401
from django.urls import reverse  # type: ignore # noqa: F401
from django.contrib.auth import authenticate, login  # type: ignore # noqa:F401
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required  # type: ignore


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
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, ' Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    return render(request, 'authors/pages/dashboard.html')
