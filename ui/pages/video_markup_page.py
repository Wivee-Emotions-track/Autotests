import time

import allure
from playwright.sync_api import Page

from ui.locators.login_page_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage


class VideoMarkupPage(DashboardPage):

    def check_page_opened(self):
        self.should_be(self.dashboard_title, contains_text="Video Markup")

    @allure.step("Check page is not empty")
    def check_page_is_not_empty(self):
        row = self.get_elements(self.table_row, contains_text='Select videos that include a person')
        assert row
