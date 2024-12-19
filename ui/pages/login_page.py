import allure
from playwright.sync_api import Page

from ui.locators.login_page_locators import LoginPageLocators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page, url):
        super().__init__(page, url=url)

    username_input = '[id="normal_login_username"]'
    password_input = '[id="normal_login_password"]'
    sign_in_btn = '[type="submit"]'
    error_msg = 'div[role="alert"]'

    @allure.step("Enter username and password")
    def login(self, username, password):
        self.type_in(self.username_input, username)
        self.type_in(self.password_input, password)
        self.click(self.sign_in_btn)

    def get_error_message(self):
        return self.get_text(self.error_msg)

    def check_error_msg(self):

        assert "Invalid Email or Password" in self.get_error_message()
