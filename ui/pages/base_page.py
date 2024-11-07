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

    def check_presence(self, locator: str, timeout=None, visible=True):
        if visible:
            self.page.wait_for_selector(selector=locator, timeout=timeout)
        else:
            self.page.wait_for_selector(selector=locator, timeout=timeout, state='hidden')

    def click(self, locator: str, timeout=None, force=True) -> None:
        self.page.locator(locator).click(timeout=timeout, force=force)

    def fill(self, locator: str, data: str, timeout=None) -> None:
        self.page.locator(locator).fill(data, timeout=timeout)

    def type_in(self, locator: str, data: str, timeout=None, press_enter=False):
        self.page.fill(locator, data, timeout=timeout)
        if press_enter:
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

    def get_elements(self, locator: str, contains_text='', index: int = None):
        list_of_elements = self.page.locator(locator).all()
        if contains_text:
            try:
                element = [element for element in list_of_elements if contains_text.lower() in
                       element.text_content().lower()][0]
            except IndexError:
                raise TimeoutError(f"Could not find element from the list of elements with text {contains_text}")

            return element
        elif index:
            element = list_of_elements[index]
            return element
        return list_of_elements
