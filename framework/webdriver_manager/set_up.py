from typing import Dict, Callable, Optional, Union

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from framework.webdriver_manager.supported import BrowserName

WebDriverOptions = Union[
    selenium.webdriver.ChromeOptions,
    selenium.webdriver.FirefoxOptions,
    selenium.webdriver.EdgeOptions,
]

installers: Dict[
    BrowserName,
    Callable[[Optional[WebDriverOptions]], WebDriver]
] = {
    BrowserName.CHROME:
        lambda options: webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                         options=options),
    BrowserName.FIREFOX:
        lambda options: webdriver.Firefox(service=Service(GeckoDriverManager().install()),
                                          options=options),
    BrowserName.EDGE:
        lambda options: webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

}


def local_driver(
        name: BrowserName = BrowserName.CHROME,
        options: WebDriverOptions = None
) -> WebDriver:
    return installers[name](options)
