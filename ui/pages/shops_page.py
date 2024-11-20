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
        if shop_name:
            assert self.get_elements(self.table_row, contains_text=shop_name), \
                f'Row with shop {shop_name} is not displayed'
        if location:
            assert self.get_elements(self.table_row, contains_text=location), \
                f'Row with location {location} is not displayed'
