from playwright.sync_api import Page

from ui.locators.platform.platform_login_page_locators import PlatformLoginPageLocators
from ui.pages.platform.platform_base_page import PlatformBasePage


class PlatformLoginPage(PlatformBasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.url += 'login'

    def login(self, username, password):
        self.fill(PlatformLoginPageLocators.EMAIL_INPUT, username)
        self.fill(PlatformLoginPageLocators.PASSWORD_INPUT, password)
        self.click(PlatformLoginPageLocators.LOG_IN_BUTTON)
