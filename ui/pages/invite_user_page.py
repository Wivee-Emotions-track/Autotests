import allure

from ui.pages.dashboard_page import DashboardPage


class InviteUserPage(DashboardPage):

    user_email_input = '[id="normal_login_email"]'
    invite_btn = '.ant-btn-primary'
    alert_message_label = '.ant-alert-message'
    password_input = '[type="password"]'
    create_password_btn = '[type="submit"]'
    sign_in_btn = '//div[contains(@class, "ant-alert-success")]/following-sibling::a'

    @allure.step("invite_user")
    def invite_user(self, user_email):
        self.type_in(self.user_email_input, user_email)
        self.click(self.invite_btn)
        self.should_be(self.alert_message_label, contains_text="Invite link has been sent to user's email.")

    @allure.step("set_password")
    def set_password(self, password):
        self.type_in(self.password_input, password)
        self.click(self.create_password_btn)
        self.should_be(self.alert_message_label, contains_text="A New Password has been set. Now you can sign in.")

    def go_to_sigh_in_page(self):
        self.click(self.sign_in_btn)
        self.check_presence(self.create_password_btn, False)