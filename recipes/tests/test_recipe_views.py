from django.urls import resolve, reverse  # type: ignore # noqa: F401
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

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

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertIs(view.func, views.category)

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
        # Agora vou checar se 'needed_title' está no meu conteúd
        self.assertIn(needed_title, content)

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
