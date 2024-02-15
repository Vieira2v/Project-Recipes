from django.urls import resolve, reverse  # type: ignore # noqa: F401
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertIs(view.func, views.category)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        # Test recipe is_published False dont show.
        recipe = self.make_recipe(is_published=False)
        # Vou executar o teste/URL agora.
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id}))
        # Agora vou checar se está aparecendo este erro abaixo qnd o
        # is_published estiver False.
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Crio uma receita.
        self.make_recipe(title=needed_title)
        # Vou executar o teste/URL agora.
        response = self.client.get(reverse('recipes:category', args=(1,)))
        # Vou converter a resposta da minha URL em uma string.
        content = response.content.decode('utf-8')
        # Agora vou checar se 'needed_title' está no meu conteúdo
        self.assertIn(needed_title, content)
