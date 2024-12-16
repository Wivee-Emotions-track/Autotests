import random
import time
from time import sleep

import allure

from ui.pages.base_page import BasePage


class DashboardPage(BasePage):

    analytics_btn = '.anticon-pie-chart'
    shop_btn = '.anticon-shop'
    alert_btn = '.anticon-notification'
    users_btn = '.anticon-user'
    api_btn = '[id="Capa_1"]'
    menu_items_list = '.ant-menu-item'
    profile_label = '.ant-avatar'
    dashboard_title = 'header .ant-typography'
    loader_label = '.ant-spin-dot'
    cell = '.ant-table-cell'
    table_row = '.ant-table-row'

    # links to pages
    alert_msg = "**/alert-messages"
    alert_rules = "**/alert-rules"
    users = "**/users"
    devices = "**/devices"
    manufactured = "**/manufactured"
    calibration = "**/calibration"
    video_markup = "**/video-markup"

    # time_selector
    hours_items_list = '[data-type="hour"] .ant-picker-time-panel-cell'
    minutes_items_list = '[data-type="minute"] .ant-picker-time-panel-cell'
    apply_time_btn = '.ant-picker-ok button'

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
        time.sleep(3)
        self.go_to_section_via_menu(section)
        self.page.wait_for_url(url)

    @allure.step("Go to api page")
    def open_api_page(self):
        time.sleep(2)
        self.click(self.api_btn)
        self.page.wait_for_url("**/tokens", timeout=10000)

    def open_users_page(self, section: str, url):
        self.click(self.users_btn)
        time.sleep(2)
        self.go_to_section_via_menu(section)
        self.page.wait_for_url(url)

    def go_to_section_via_menu(self, section: str):
        self.check_presence(self.menu_items_list)
        menu_item = self.get_elements(self.menu_items_list, contains_text=section)
        menu_item.click()

    @allure.step("Check that we were logged in")
    def check_logged_in(self):
        assert self.page.is_visible(self.profile_label, timeout=5), \
            'Failed to log in with valid username and password'

    @allure.step("select time in time input")
    def select_time(self, start_time_input_locator, end_time_input_locator, apply=False):

        start_time = []
        end_time = []
        self.click(start_time_input_locator)
        self.check_presence(self.hours_items_list)
        hours_list_items = self.get_elements(self.hours_items_list)
        minutes_list_items = self.get_elements(self.minutes_items_list)

        # Получаем рандомный элемент времени (часы и минуты) и запоминаем значения
        begin_hour_element = random.choice(hours_list_items[:-1])
        begin_minute_element = random.choice(minutes_list_items[:-1])
        start_time.append(begin_hour_element.text_content())
        start_time.append(begin_minute_element.text_content())

        begin_hour_element.click()
        begin_minute_element.click()
        if apply:
            self.click(self.apply_time_btn)

        begin_hour_element_index = hours_list_items.index(begin_hour_element)
        begin_minute_element_index = minutes_list_items.index(begin_minute_element)

        # Получаем элементы времени, которые будут позже чем выбранное ранее время начала и запоминаем его
        end_hour_element = (
            hours_list_items)[begin_hour_element_index + 1]
        end_minute_element = (
            minutes_list_items)[begin_minute_element_index + 1]

        self.click(end_time_input_locator)
        end_time.append(end_hour_element.text_content())
        end_time.append(end_minute_element.text_content())
        end_hour_element.click()
        end_minute_element.click()
        if apply:
            self.click(self.apply_time_btn)

        return start_time, end_time

    def check_loader_absence(self):
        self.check_presence(self.loader_label, False)
