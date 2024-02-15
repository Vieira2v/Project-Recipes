from django.urls import resolve, reverse  # type: ignore # noqa: F401
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    # Função para testar a URL de SEARCH.
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    # Função para renderizar o SEARCH
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=Teste'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;Teste&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )

    # Na response1 eu vou buscar pelo title1.
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
    # Na response2 eu vou buscar pelo title2.
        response2 = self.client.get(f'{search_url}?q={title2}')
    # E aqui vou qrer ambas.
        response_both = self.client.get(f'{search_url}?q=this')
    # Aqui vou ver se na recipe1 eu irei ter a response1.
        self.assertIn(recipe1, response1.context['recipes'])
    # Aqui vou ver se na recipe2 eu não irei ter a response1.
        self.assertNotIn(recipe2, response1.context['recipes'])
    # Aqui estou fazendo a mesma coisa de cima só q invertido.
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
