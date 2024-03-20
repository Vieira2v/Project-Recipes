from selenium import webdriver  # noqa: F401
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == 1:
        chrome_options.add_argument('--headless')

    chrome_service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=chrome_service)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('http://www.udemy.com/')
    sleep(10)
    browser.quit()
