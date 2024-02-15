from django.urls import resolve, reverse  # type: ignore # noqa: F401
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipes(self):
        needed_title = 'This is a detail page - It load one recipe'
        # Crio uma receita.
        self.make_recipe(title=needed_title)
        # Vou executar o teste/URL agora.
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        # Vou converter a resposta da minha URL em uma string.
        content = response.content.decode('utf-8')
        # Agora vou checar se 'needed_title' está no meu conteúd
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        # Test recipe is_published False dont show.
        recipe = self.make_recipe(is_published=False)
        # Vou executar o teste/URL agora.
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))
        # Agora vou checar se está aparecendo este erro abaixo qnd o
        # is_published estiver False.
        self.assertEqual(response.status_code, 404)
