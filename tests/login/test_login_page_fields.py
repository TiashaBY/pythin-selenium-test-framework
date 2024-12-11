import time
import unittest
import pytest
import softest

from pages.login.login_page import LoginPage
from tests.conftest import browser_driver, testdata_path
from ddt import ddt, data, file_data, unpack


# This is an example of test with soft asserts
@ddt
@pytest.mark.usefixtures("browser_driver")
class LoginPageFieldsTest(softest.TestCase):

    @file_data("../../testdata/login_page_fields.json")
    def test_incorrect_password_length(self, login, password, show_password_error, password_error_text, show_login_error, login_error_text):
        login_page = LoginPage(self.browser)
        login_page.open()
        login_page.type_login(login)
        login_page.type_password(password)
        login_page.click_login_button()
        time.sleep(1)

        if show_login_error:
            self.soft_assert(self.assertTrue, login_page.login_hint_visibility)
            self.soft_assert(self.assertEqual, login_error_text, login_page.login_hint_text())
        else:
            self.soft_assert(self.assertFalse, login_page.login_hint_visibility)

        if show_password_error:
            self.soft_assert(self.assertTrue, login_page.password_hint_visibility)
            self.soft_assert(self.assertEqual, password_error_text, login_page.password_hint_text())
        else:
            self.soft_assert(self.assertFalse, login_page.password_hint_visibility)

        self.assert_all()

