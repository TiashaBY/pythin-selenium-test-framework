import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.login.gmail_login_popup import GmailLoginPopup
from pages.timer.timer_page import TimerPage

root_id = (By.ID, "root")

login_gmail_button = (By.XPATH, '//*[@id="root"]//button[normalize-space()="Login with Google"]')
login_gmail_window_name = "Google"

login_edit = (By.ID, "email")
login_hint = (By.ID, "email_help")

password_edit = (By.ID, "password")
password_hint = (By.ID, "password_help")

login_button = (By.XPATH, '//button[normalize-space()="Login"]')


class LoginPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    def open(self):
        self.browser.get(f"{self.base_url}/login")
        self.wait_element_is_visible(root_id)

    def type_login(self, login):
        self.find_by(login_edit).clear()
        self.find_by(login_edit).send_keys(login)

    def type_password(self, password):
        self.find_by(password_edit).clear()
        self.find_by(password_edit).send_keys(password)

    def click_login_button(self):
        self.wait_and_click(login_button)

    def login_with_gmail(self):
        time.sleep(2)
        self.open_new_window(login_gmail_button)
        self.switch_to_window(login_gmail_window_name)
        return GmailLoginPopup(self.browser)

    @property
    def password_hint_visibility(self):
        try:
            return self.wait_element_is_visible(password_hint)
        except TimeoutException:
            return False

    @property
    def login_hint_visibility(self) -> bool:
        try:
            return self.wait_element_is_visible(login_hint)
        except TimeoutException:
            return False

    def login_hint_text(self) -> str:
        return self.find_by(login_hint).text

    def password_hint_text(self) -> str:
        self.wait_for_element_not_empty(password_hint)
        return self.find_by(password_hint).text

    def login(self, login, password):
        self.type_login(login)
        self.type_password(password)
        current_url = self.get_url()
        self.click_login_button()
        self.wait_for_redirect(current_url)
        return TimerPage(self.browser)
