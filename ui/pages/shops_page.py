import allure

from ui.pages.dashboard_page import DashboardPage


class ShopsPage(DashboardPage):

    add_shop_btn = '.ant-row .ant-btn-icon'
    search_shop_btn = '(//span[contains(@class, "anticon-search")])[1]'
    search_input = '.ant-table-filter-dropdown input'
    start_search_btn = '.ant-btn-primary'
    table_row = '.ant-table-row'

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
        assert self.get_elements(self.table_row, contains_text=shop_name), f'Row with shop {shop_name} is not displayed'
