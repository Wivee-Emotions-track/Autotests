import allure
from playwright.sync_api import Page

from ui.locators.login_page_locators import LoginPageLocators
from ui.pages.base_page import BasePage


class AlertRules(BasePage):

    alert_rules_table = '.ant-spin-nested-loading'

    def check_page_opened(self):
        self.check_presence(self.alert_rules_table)
