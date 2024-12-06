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
            self.url = url
        self.page.goto(self.url)

    def check_presence(self, locator: str, visible=True, timeout=None):
        if visible:
            self.page.wait_for_selector(selector=locator, timeout=timeout, state='visible')
        else:
            self.page.wait_for_selector(selector=locator, timeout=timeout, state='hidden')

    def click(self, locator: str, timeout=None, force=True) -> None:
        element = self.page.locator(locator)
        element.scroll_into_view_if_needed()
        element.click(timeout=timeout, force=force)

    def fill(self, locator: str, data: str, timeout=None) -> None:
        self.page.locator(locator).fill(data, timeout=timeout)

    def type_in(self, locator: str, data: str, timeout=None, press_enter=False):
        self.page.fill(locator, data, timeout=timeout)
        if press_enter:
            self.page.press(locator, "Enter")

    def get_text(self, locator: str, input=False, attribute='', index=0, timeout=None) -> str:
        if input:
            return self.page.locator(locator).nth(index).input_value(timeout=timeout)
        if attribute:
            return self.page.locator(locator).nth(index).get_attribute(attribute)
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
        list_of_elements = self.page.locator(locator).all()  # todo hastext
        if contains_text:
            try:
                element = [element for element in list_of_elements if contains_text.lower() in
                           element.text_content().lower()][0]
            except IndexError:
                return None
                # raise TimeoutError(f"Could not find element from the list of elements with text {contains_text}")

            return element
        elif index is not None:
            try:
                element = list_of_elements[index]  # todo нормальное ожидание впилить
            except IndexError:
                return None
            return element
        return list_of_elements

    def get_child_element(self, parent_element, child_locator):
        child_element = parent_element.locator(child_locator)
        return child_element

    def get_childs_element(self, parent_element, child_locator):
        child_element = parent_element.locator(child_locator).all()
        return child_element

    def should_be(self, locator, contains_text='', input=False):

        element_text = self.get_text(locator, input=input)

        if contains_text:

            assert contains_text.lower() in element_text.lower(), \
                f'No text {contains_text} in element {locator},' \
                f' displayed text is {element_text}'
