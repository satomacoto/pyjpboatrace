from abc import ABCMeta, abstractmethod
from logging import Logger, getLogger
from typing import Any, Callable, Dict

import requests
from selenium import webdriver


class BaseScraper(metaclass=ABCMeta):
    """Base class for scraper."""

    def __init__(
        self,
        driver: webdriver.remote.webdriver.WebDriver,
        parser: Callable[
            [
                str,
            ],
            Dict[str, Any],
        ],
        logger: Logger = getLogger(__name__),
    ):
        self._driver = driver
        self._parser = parser
        self._logger = logger

    @classmethod
    @abstractmethod
    def make_url(cls, *args, **kwargs) -> str:
        raise NotImplementedError()

    def get(self, *args, **kwargs) -> Dict[str, Any]:
        if self._driver is None:
            return self._requests_get(*args, **kwargs)

        return self._driver_get(*args, **kwargs)

    def _driver_get(self, *args, **kwargs) -> Dict[str, Any]:
        url = self.make_url(*args, **kwargs)
        self._logger.info(f"URL created: {url}")
        self._driver.get(url)
        html = self._driver.page_source
        return self._parser(html)

    def _requests_get(self, *args, **kwargs) -> Dict[str, Any]:
        url = self.make_url(*args, **kwargs)
        self._logger.info(f"URL created: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f"Invalid status code: {response.status_code}")
        return self._parser(response.text)
