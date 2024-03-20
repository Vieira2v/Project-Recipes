from utils.browser import make_chrome_browser
from django.test import LiveServerTestCase  # type: ignore
import time


class RecipeBaseFunctionalTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
