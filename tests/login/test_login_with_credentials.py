import unittest

import pytest
from ddt import ddt, file_data

from pages.login.login_page import LoginPage
from tests.conftest import browser_driver


@ddt
@pytest.mark.usefixtures("browser_driver")
class LoginWithCredentialsTest(unittest.TestCase):

    @file_data("../../testdata/users.json")
    def test_login_with_credentials(self, login, password):
        login_page = LoginPage(self.browser)
        login_page.open()
        timer_page = login_page.login(login, password)
        assert "timer" in timer_page.get_url(), "Timer page didn't open"


