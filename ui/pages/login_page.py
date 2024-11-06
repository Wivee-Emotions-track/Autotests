import allure
from playwright.sync_api import Page

from configs.config import BASE_URL
from ui.locators.login_page_locators import LoginPageLocators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page,
                         url=BASE_URL)

    username_input = '[id="normal_login_username"]'
    password_input = '[id="normal_login_password"]'
    sign_in_btn = '[type="submit]'
    error_msg = 'div[role="alert"]'

    @allure.step("Enter username and password")
    def login(self, username, password):
        self.type_in(self.username_input, username)
        self.type_in(self.password_input, password)
        self.click(self.sign_in_btn)

    def get_error_message(self):
        return self.page.inner_text(LoginPageLocators.ERROR_MESSAGE)

    def check_logged_in(self):
        if not self.page.is_visible(LoginPageLocators.PROFILE_LABEL):
            assert self.page.is_visible(LoginPageLocators.PROFILE_LABEL), \
                'Failed to log in with valid username and password'

            assert "You can use a sign-in code, reset your password or try again" in self.get_error_message(), \
                   "No message for invalid username and password"
