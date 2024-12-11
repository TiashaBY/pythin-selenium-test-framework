from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import settings

TIMEOUT = settings.timeout


class BasePage:
    base_url = settings.base_url

    def __init__(self, browser):
        self.browser = browser

    def find_by(self, locator):
        return self.browser.find_element(*locator)

    def get_url(self):
        return self.browser.current_url

    def wait_element_is_visible(self, locator):
        return WebDriverWait(self.browser, TIMEOUT).until(
            EC.visibility_of_element_located(locator))

    def wait_for_element_not_present(self, args):
        element = WebDriverWait(self.browser, TIMEOUT).until(
            EC.invisibility_of_element(args)
        )
        return element

    def wait_for_element_not_empty(self, locator: tuple[str, str]):
        WebDriverWait(self.browser, TIMEOUT).until(lambda a: self.find_by(locator).text.strip() != '')

    def wait_and_click(self, locator):
        element = WebDriverWait(self.browser, TIMEOUT).until(
            EC.all_of(EC.visibility_of_element_located(locator), EC.element_to_be_clickable(locator))
        )[0]
        element.click()

    def open_new_window(self, button_locator) -> bool:
        handles = self.browser.window_handles
        self.wait_and_click(button_locator)
        try:
            WebDriverWait(self.browser, TIMEOUT).until(
                EC.new_window_is_opened(handles)
            )
            return True
        except:
            return False

    def switch_to_window(self, window_title):
        main_window = self.browser.current_window_handle
        for handle in self.browser.window_handles:
            if handle != main_window:
                popup = handle
                self.browser.switch_to.window(popup)
                if window_title in self.browser.title:
                    break
                else:
                    continue

    def wait_for_redirect(self, old_url):
        WebDriverWait(self.browser, TIMEOUT).until(EC.url_changes(old_url))
