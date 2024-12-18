import time

import allure
from playwright.sync_api import Page

from ui.locators.login_page_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage


class CalibrationPage(DashboardPage):

    def check_page_opened(self):

        self.check_presence(self.cell)
        self.should_be(self.dashboard_title, contains_text="Calibration")

    @allure.step("Check table cells is not empty")
    def check_table_is_not_empty(self):
        self.check_presence(self.table_row)
        time.sleep(2)  # todo
        row = self.get_elements(self.table_row, contains_text='Delete device')
        assert row
