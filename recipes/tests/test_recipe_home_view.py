from django.urls import resolve, reverse  # type: ignore # noqa: F401
from recipes import views
from unittest.mock import patch
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here... 👎 </h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        # Vou executar o teste/URL agora.
        response = self.client.get(reverse('recipes:home'))
        # Vou converter a resposta da minha URL em uma string.
        content = response.content.decode('utf-8')
        # Vou checar o número de receitas no meu context.
        response_context_recipes = response.context['recipes']
        # Agora vou checar se nesse meu conteudo tem o Recipe Title.
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
# Se o meu numero de receitas for diferente de 1, meu teste ira dar erro.
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        # Test recipe is_published False dont show.
        self.make_recipe(is_published=False)
        # Vou executar o teste/URL agora.
        response = self.client.get(reverse('recipes:home'))
        # Agora vou checar se está aparecendo esta frase abaixo qnd o
        # is_published estiver False.
        self.assertIn(
            '<h1>No recipes found here... 👎 </h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_is_paginated(self):
        # 9 receitas vão ter no site.
        for i in range(9):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        # Em cada página vai ter 3 receitas
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        # Página 1, tem 3 receitas?
        self.assertEqual(len(paginator.get_page(1)), 3)
        # Página 2, tem 3 receitas?
        self.assertEqual(len(paginator.get_page(2)), 3)
        # Página 3, tem 3 receitas?
        self.assertEqual(len(paginator.get_page(3)), 3)
