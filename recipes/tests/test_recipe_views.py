from django.test import TestCase  # type: ignore # noqa: F401
from django.urls import resolve, reverse  # type: ignore # noqa: F401
from recipes import views
from recipes.models import Category, Recipe, User  # type: ignore # noqa: F401


class RecipeViewsTest(TestCase):

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
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(  # noqa: F841
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
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

    def test_recipe_home_view_function_is_correct(self):
        view = resolve('/')
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)
