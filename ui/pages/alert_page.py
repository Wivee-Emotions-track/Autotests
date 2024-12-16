import allure
from playwright.sync_api import Page

from ui.locators.login_page_locators import LoginPageLocators
from ui.pages.base_page import BasePage


class AlertPage(BasePage):

    true_positive_label = '.ant-typography-success'

    def check_page_opened(self):
        self.check_presence(self.true_positive_label)
