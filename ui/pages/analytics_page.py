from time import sleep

import allure

from ui.locators.analytics_page_locators import AnalyticsPageLocators
from ui.pages.base_page import BasePage

filename = 'DataAnalytics-2024-07-03-2024-07-15'


class AnalyticsPage(BasePage):

    graphics_btn = '[data-icon="line-chart"]'
    table_btn = '[data-icon="table"]'

    export_btn = '.ant-flex-justify-space-between .ant-btn-primary'
    export_file_name_input = '[id="report-settings_fileName"]'

    # settings
    settings_btn = '[data-icon="setting"]'
    settings_form = '.ant-drawer-content'
    switchers_list = '.ant-drawer-content .ant-space'
    switcher = '[role="switch"]'
    save_btn = '//span[text()="Save"]'

    # table
    column_sorter = '.ant-table-column-sorters'
    comparison_dropdown = '.ant-space .ant-dropdown-trigger'
    comparison_menu_item = '.ant-dropdown-menu-item'
    cell = '.ant-table-cell'

    # date filter
    filter_days = '//div[contains(@class, "ant-picker-presets")]//li'
    start_date_input = '[placeholder="Start date"]'
    end_date_input = '[placeholder="End date"]'

    chart_label = '.plot-container'
    download_btn = '[type="submit"]'
    download_form = '.ant-modal-content'

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

    @allure.step("switch column presence")
    def switch_menu_column(self, column_name: str):
        element = self.get_elements(self.switchers_list, column_name)
        switcher = self.get_child_element(element, self.switcher)
        switcher.click()

    @allure.step("save table settings")
    def save_settings(self):
        self.click(self.save_btn)
        self.check_presence(self.settings_form)

    @allure.step("check_column_presence after settings changing")
    def check_column_presence(self, column_name, presence=False):
        column = self.get_elements(self.column_sorter, column_name)
        if not presence:
            assert column is None, f'Column with name {column_name} should not be displayed'
        else:
            assert column is not None, f'Column with name {column_name} should be displayed'

    @allure.step("Select comparison type")
    def select_comparison(self, comparison_type):
        self.click(self.comparison_dropdown)
        comparyson = self.get_elements(self.comparison_menu_item, comparison_type)
        comparyson.click()

    @allure.step("check_comparison_module_is_active")
    def check_comparison_module_is_active(self):

        cell = self.get_elements(self.cell, index=15)
        assert "%" in cell.inner_text(), 'Compare module wasn`t added'
