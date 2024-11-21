import time

import allure

from ui.pages.dashboard_page import DashboardPage


class UsersPage(DashboardPage):

    add_user_btn = '.ant-btn [aria-label="user-add"]'
    delete_user_btn = '.ant-btn-dangerous'
    edit_user_btn = '.ant-btn-primary'
    search_btn = '(//span[contains(@class, "anticon-search")])[1]'
    search_input = '.ant-table-filter-dropdown input'
    start_search_btn = '.ant-table-filter-dropdown .ant-btn-primary'
    confirm_delete_btn = '.ant-popconfirm-buttons .ant-btn-primary'
    shop_in_table_item = '.ant-table-row .ant-space-item .ant-typography'

    @allure.step("Add user")
    def add_user(self):
        self.click(self.add_user_btn)
        self.check_presence(self.add_user_btn, visible=False)

    @allure.step("Search user")
    def search_user(self, user_name: str, positive=True):

        self.check_presence(self.search_btn)
        self.click(self.search_btn)
        self.type_in(self.search_input, user_name)
        self.click(self.start_search_btn)
        self.check_search_result(user_name, positive)

    @allure.step("Delete user")
    def delete_user(self, user_email: str):
        row = self.get_elements(self.table_row, user_email)
        delete = self.get_child_element(row, self.delete_user_btn)
        delete.click()
        self.click(self.confirm_delete_btn)
        self.check_presence(self.confirm_delete_btn, False)

    def edit_user(self):
        self.click(self.edit_user_btn)
        self.check_presence(self.table_row, False)

    def check_search_result(self, user_name, positive=True):
        if positive:
            assert self.get_elements(self.table_row, contains_text=user_name), \
                f'Row with user {user_name} is not displayed'
        else:
            assert None, f'User {user_name} is not deleted'

    def check_page_opened(self):
        self.should_be(self.dashboard_title, contains_text="Shops")
        self.check_presence(self.add_user_btn)
