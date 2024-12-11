import os
from typing import Literal, Optional

import pydantic_settings

from framework.utils import abs_path_from_project
from framework.webdriver_manager import supported

EnvContext = Literal['test', 'prod']


class Settings(pydantic_settings.BaseSettings):
    context: EnvContext = 'test'
    base_url: str = ''
    timeout: float = 6.0
    browser_name: supported.BrowserName = supported.BrowserName.CHROME
    maximize_window: bool = True
    save_page_source_on_failure: bool = True
    headless: bool = False
    keep_browser_open: bool = False

    # todo for selenoid
    remote_url: Optional[str] = None
    remote_version: Optional[str] = None
    remote_platform: Optional[str] = None
    remote_enableVNC: bool = True
    remote_screenResolution: str = '1920x1080x24'
    remote_enableVideo: bool = False
    remote_enableLog: bool = True

    @classmethod
    def with_context(cls, env: Optional[EnvContext] = None) -> 'Settings':
        """
        factory method to init Settings with values from corresponding .env file
        """
        asked_or_current = env or cls().context
        return cls(_env_file=abs_path_from_project(
            f'.{asked_or_current}.env'
        ))


settings = Settings()
