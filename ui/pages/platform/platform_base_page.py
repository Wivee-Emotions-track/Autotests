from playwright.sync_api import Page
from pytest_check import check

from ui.locators.platform.platform_base_locators import PlatformBaseLocators
from ui.pages.base_page import BasePage

from playwright._impl._errors import TimeoutError


class PlatformBasePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page,
                         url='https://platform-front.snmt.dev/')

    def check_alert_message(self, text):
        """Soft check alert message equal text."""
        try:
            message = self.get_text(PlatformBaseLocators.ALERT_MESS, timeout=3000)
            check.equal(message, text, f'Expected message: {text} Actual: {message}')
        except TimeoutError:
            check.is_true(False, f'No alert message with locator: {PlatformBaseLocators.ALERT_MESS}')
