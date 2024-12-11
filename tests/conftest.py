import pytest

from selenium.webdriver.remote.webdriver import WebDriver

from framework import webdriver_manager
import config
from framework.utils import abs_path_from_project
from framework.webdriver_manager import supported
from framework.webdriver_manager.set_up import WebDriverOptions


@pytest.fixture(scope='module')
def testdata_path():
    context = config.settings.context
    return abs_path_from_project(
        f'/testdata/{context}'
    )


@pytest.fixture(scope='function', autouse=False)
def browser_driver(request):
    browser: WebDriver = _driver_from(config.settings)
    browser.implicitly_wait(config.settings.timeout)
    browser.save_page_source_on_failure = (
        config.settings.save_page_source_on_failure
    )
    if request.cls is not None:
        request.cls.browser = browser
    yield browser
    if not config.settings.keep_browser_open:
        browser.quit()


def _driver_from(settings: config.Settings) -> WebDriver:
    driver_options = _driver_options_from(settings)

    from selenium import webdriver

    driver = (webdriver_manager.set_up.local_driver(
            settings.browser_name,
            driver_options,
        )
        if not settings.remote_url
        else webdriver.Remote(
            command_executor=settings.remote_url,
            options=driver_options,
        )
    )

    if settings.maximize_window:
        driver.maximize_window()
    else:
        driver.set_window_size(
            width=settings.window_width,
            height=settings.window_height,
        )

    return driver


def _driver_options_from(settings: config.Settings) -> WebDriverOptions:
    options = None

    from selenium import webdriver

    if settings.browser_name == supported.BrowserName.CHROME:
        options = webdriver.ChromeOptions()
        options.headless = settings.headless

    if settings.browser_name == supported.BrowserName.FIREFOX:
        options = webdriver.FirefoxOptions()
        options.headless = settings.headless

    if settings.browser_name == supported.BrowserName.EDGE:
        options = webdriver.EdgeOptions()
        options.ignore_local_proxy_environment_variables()

    if settings.remote_url:
        options.set_capability(
            'screenResolution', settings.remote_screenResolution
        )
        options.set_capability('enableVNC', settings.remote_enableVNC)
        options.set_capability('enableVideo', settings.remote_enableVideo)
        options.set_capability('enableLog', settings.remote_enableLog)
        if settings.remote_version:
            options.set_capability('version', settings.remote_version)
        if settings.remote_platform:
            options.set_capability('platform', settings.remote_platform)

    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")

    return options
