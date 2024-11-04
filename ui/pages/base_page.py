import os

import allure
from playwright.sync_api import Page

from configs.project_paths import SCREENSHOTS_PATH


class BasePage:

    def __init__(self, page: Page, url=None):
        self.page = page
        self.url = url

    def open(self, url=None) -> None:
        if url:
            self.page.goto(url)
        else:
            self.page.goto(self.url)

    def wait_for_selector(self, locator: str, timeout=None):
        self.page.wait_for_selector(selector=locator, timeout=timeout)

    def click(self, locator: str, timeout=None) -> None:
        self.page.locator(locator).click(timeout=timeout)

    def fill(self, locator: str, data: str, timeout=None) -> None:
        self.page.locator(locator).fill(data, timeout=timeout)

    def enter_value(self, locator: str, data: str, timeout=None):
        self.page.fill(locator, data, timeout=timeout)
        self.page.press(locator, "Enter")

    def get_text(self, locator: str, index=0, timeout=None) -> str:
        return self.page.locator(locator).nth(index).text_content(timeout=timeout)

    def get_url(self) -> str:
        return self.page.url

    def checkbox(self, locator: str) -> None:
        self.page.locator(locator).check()

    def screenshot(self, file_name:str, allure_posting:bool = True):
        screenshot_path = os.path.join(SCREENSHOTS_PATH, file_name)
        self.page.screenshot(path=screenshot_path)
        if allure_posting:
            allure.attach.file(screenshot_path, name=file_name, attachment_type=allure.attachment_type.PNG)

    def reload(self, timeout=None):
        self.page.reload(timeout=timeout)
