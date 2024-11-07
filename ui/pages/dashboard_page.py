import time
from time import sleep

import allure

from ui.pages.base_page import BasePage


class Dashboard(BasePage):

    analytics_btn = '.anticon-pie-chart'
    shop_btn = '.anticon-shop'
    alert_btn = '.anticon-notification'
    users_btn = '.anticon-user'
    api_btn = '[id="Capa_1"]'
    menu_items_list = '.ant-menu-item'
    profile_label = '.ant-avatar'

    # links to pages
    alert_msg = "**/alert-messages"
    alert_rules = "**/alert-rules"
    users = "**/users"
    devices = "**/devices"
    manufactured = "**/manufactured"
    calibration = "**/calibration"
    video_markup = "**/video-markup"

    @allure.step("Go to analytics page")
    def open_analytics_page(self):
        self.click(self.analytics_btn)
        self.page.wait_for_url("**/analytics")
        sleep(1)

    @allure.step("Go to shops page")
    def open_shops_page(self):
        self.click(self.shop_btn)
        self.page.wait_for_url("**/shops")
        sleep(1)

    def open_alerts_page(self, section, url):
        self.click(self.alert_btn)
        time.sleep(2)
        self.go_to_section_via_menu(section)
        self.page.wait_for_url(url)

    @allure.step("Go to api page")
    def open_api_page(self):
        self.click(self.api_btn)
        self.page.wait_for_url("**/tokens")

    def open_users_page(self, section: str, url):
        self.click(self.users_btn)
        time.sleep(2)
        self.go_to_section_via_menu(section)
        self.page.wait_for_url(url)

    def go_to_section_via_menu(self, section: str):
        menu_item = self.get_elements(self.menu_items_list, contains_text=section)
        menu_item.click()

    @allure.step("Check that we were logged in")
    def check_logged_in(self):
        if not self.page.is_visible(self.profile_label):
            assert self.page.is_visible(self.profile_label), \
                'Failed to log in with valid username and password'
