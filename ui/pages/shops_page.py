import time

import allure

from ui.pages.dashboard_page import DashboardPage


class ShopsPage(DashboardPage):

    add_shop_btn = '.ant-row .ant-btn-icon'
    search_shop_btn = '(//span[contains(@class, "anticon-search")])[1]'
    search_shop_location_btn = '(//span[contains(@class, "anticon-search")])[2]'
    search_input = '.ant-table-filter-dropdown input'
    start_search_btn = '.ant-btn-primary'
    table_row = '.ant-table-row'
    edit_shop_btn = '.ant-table-cell .ant-btn'
    shop_in_table_item = '.ant-table-row .ant-space-item .ant-typography'
    next_page_btn = '.ant-pagination-next'

    @allure.step("add shop")
    def add_shop(self):
        self.click(self.add_shop_btn)
        self.check_presence(self.add_shop_btn, visible=False)

    @allure.step("search shop")
    def search_shop(self, shop_name: str):

        self.check_presence(self.search_shop_btn)
        self.click(self.search_shop_btn)
        self.type_in(self.search_input, shop_name)
        self.click(self.start_search_btn)

    @allure.step("search shop via location")
    def search_shop_via_location(self, location: str):

        self.check_presence(self.search_shop_btn)
        self.click(self.search_shop_location_btn)
        self.type_in(self.search_input, location)
        self.click(self.start_search_btn)

    def edit_shop(self):
        self.click(self.edit_shop_btn)
        self.check_presence(self.table_row, False)

    def open_shop(self, shop_name):

        self.get_elements(self.shop_in_table_item, contains_text=shop_name).click()

    def check_search_result(self, shop_name='', location=''):
        for page in range(10):
            self.click(self.next_page_btn)
            if self.get_elements(self.table_row):
                break
        if shop_name:
            assert self.get_elements(self.table_row, contains_text=shop_name), \
                f'Row with shop {shop_name} is not displayed'
        if location:
            assert self.get_elements(self.table_row, contains_text=location), \
                f'Row with location {location} is not displayed'

    @allure.step("Check table cells is not empty")
    def check_table_is_not_empty(self, shops):
        self.check_presence(self.table_row)
        time.sleep(5)  # todo
        for shop_name in shops:
            row = self.get_elements(self.table_row, contains_text=shop_name)
            cells = self.get_childs_element(row, self.cell)[:-1]
            for cell in cells:
                assert cell.text_content() != '', f'No data for shop {shop_name}'

    def check_page_opened(self):
        self.check_presence(self.cell)
        self.should_be(self.dashboard_title, contains_text="Shops")
        self.check_presence(self.edit_shop_btn)
