import allure

from ui.pages.dashboard_page import DashboardPage


class TokensPage(DashboardPage):

    add_token_btn = '[id="add-api-token"]'
    token_name_input = '[id="validateOnly_name"]'
    add_btn = '.ant-btn-primary'
    table_row = '.ant-table-row'
    hide_eye_label = '[data-icon="eye-invisible"]'
    token_input = '.ant-input-password input'
    revoke_token_btn = '.ant-btn-dangerous'
    revoke_message_label = '.ant-popconfirm-description'
    confirm_revoke_btn = '.ant-popconfirm-buttons .ant-btn-primary'


    @allure.step("add token")
    def add_token(self, token_name):
        self.click(self.add_token_btn)
        self.type_in(self.token_name_input, token_name)
        self.click(self.add_btn)
        self.check_presence(self.token_name_input, visible=False)

    @allure.step("Get created token")
    def get_created_token(self, token_name: str):
        row = self.get_elements(self.table_row, token_name)
        eye = self.get_child_element(row, self.hide_eye_label)
        eye.click()
        token_element = self.get_child_element(row, self.token_input)
        token = token_element.input_value()
        return token

    @allure.step("Revoke token")
    def revoke_token(self, token_name):
        row = self.get_elements(self.table_row, token_name)
        self.get_child_element(row, self.revoke_token_btn).click()
        self.should_be(self.revoke_message_label, 'Are you sure you want to revoke this token?'
                                                  ' You will not be able to use it once it is revoked.')
        self.click(self.confirm_revoke_btn)

    def check_page_opened(self):
        self.should_be(self.dashboard_title, contains_text="API tokens")
