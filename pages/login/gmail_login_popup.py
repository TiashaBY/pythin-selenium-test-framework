from selenium.webdriver.common.by import By

from pages.base_page import BasePage

login_edit = (By.ID, "identifierId")
next_button = (By.XPATH, '//button[normalize-space()="Next"]')


class GmailLoginPopup(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    def type_login(self, name):
        login_box = self.find_by(login_edit)
        login_box.send_keys(name)

    def click_next(self):
        self.wait_and_click(next_button)
