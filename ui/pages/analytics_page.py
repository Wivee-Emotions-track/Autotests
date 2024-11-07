from time import sleep

import allure

from ui.locators.analytics_page_locators import AnalyticsPageLocators
from ui.pages.base_page import BasePage

filename = 'DataAnalytics-2024-07-03-2024-07-15'


class AnalyticsPage(BasePage):

    graphics_btn = '[data-icon="line-chart"]'
    table_btn = '[data-icon="table"]'
    settings_btn = '[data-icon="setting"]'
    export_btn = '.ant-flex-justify-space-between .ant-btn-primary'
    export_file_name_input = '[id="report-settings_fileName"]'
    settings_form = '.ant-drawer-content'
    switchers_list = '[role="switch"]'
    column_sorter = '.ant-table-column-sorters'
    chart_label = '.plot-container'
    download_btn = '[type="submit"]'
    download_form = '.ant-modal-content'

    def click_table(self):
        self.page.click(AnalyticsPageLocators.TABLE_BUTTON)
        self.page.wait_for_load_state()
        sleep(2)

    @allure.step("open_chart")
    def open_graphics(self):
        self.click(self.graphics_btn)
        self.check_presence(self.chart_label)

    @allure.step("open_table")
    def open_table(self):
        self.click(self.table_btn)
        self.check_presence(self.chart_label)

    @allure.step("open_settings")
    def open_settings(self):
        self.click(self.settings_btn)
        self.check_presence(self.settings_form)

    @allure.step("export data")
    def export_data(self, file_name):
        self.click(self.export_btn)
        self.check_presence(self.download_form)
        self.type_in(self.export_file_name_input, file_name)
        self.click(self.download_btn)
        self.check_presence(self.export_file_name_input, visible=False)
