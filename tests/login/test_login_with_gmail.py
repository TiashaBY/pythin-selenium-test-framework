import pytest

from pages.login.login_page import LoginPage
from tests.conftest import browser_driver

login = "test@gmail.com"


def test_login_with_gmail(browser_driver):
    login_page = LoginPage(browser_driver)
    login_page.open()

    gmail_page = login_page.login_with_gmail()

    gmail_page.type_login(login)
    gmail_page.click_next()
    # todo get correct creds and assert the redirect
