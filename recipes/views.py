from django.shortcuts import render, get_object_or_404  # type:ignore
from recipes.models import Recipe
from django.http import Http404     # type:ignore
from django.db.models import Q   # type: ignore # noqa: F401
from django.core.paginator import Paginator  # type: ignore # noqa: F401
from utils.pagination import make_pagination
import os

PER_PAGES = os.environ.get('PER_PAGE')


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(category__id=category_id,
                                    is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    if not recipes:
        raise Http404('Not found')

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes.first().category.name} - Category |'
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        # Aqui qnd o usuário pesquisar alguma palavra, o meu site vai
        # mostrar pra ele todas as receitas q tem esta palavra no
        # titulo ou na descrição, idependente se ta de letra maius ou minus.
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')
    # Agora vou ordenar pelo id de forma decrescente para ficar em primeiro
    # as receitas publicadas mais recentes.

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}"',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
