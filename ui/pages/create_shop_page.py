import time
from time import sleep

import allure

from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage


class CreateShopPage(DashboardPage):

    upload_plan_input = '.ant-upload input'
    uploaded_plan = '.konvajs-content'
    zones_items_list = '.ant-flex-justify-space-between .ant-typography'
    continue_btn = '.ant-btn-primary'

    shop_name_input = '[id="name"]'
    shop_location_input = '[id="location"]'
    shop_timezone_input = '[id="timeZone"]'
    timezone_list_item = '.ant-select-item'
    shop_industry = '[id="industry"]'
    industry_list_item = '.ant-select-item'
    shop_traffic = '[id="traffic"]'
    traffic_list_item = '.ant-select-item'
    congrats_panel = '.ant-modal-content'
    got_it_btn = '.ant-modal-content .ant-btn-primary'
    save_changes_label = '[aria-label="check-circle"]'

    # open hours
    open_hours_start_input = '[id="openHours"]'
    open_hours_end_input = '//input[@id="openHours"]/..//following-sibling::div/input'
    open_hours_weekend_start_input = '[id="openHoursWeekend"]'
    open_hours_weekend_end_input = '//input[@id="openHoursWeekend"]/..//following-sibling::div/input'
    save_shop_btn = '[type="submit"]'

    @allure.step("upload plan")
    def upload_plan(self, path_to_plan):
        self.page.set_input_files(self.upload_plan_input, path_to_plan)
        self.check_presence(self.uploaded_plan)

    @allure.step("go_to_shop_details")
    def go_to_shop_details(self):
        self.click(self.continue_btn)
        self.check_presence(self.shop_name_input)

    @allure.step("fill_shop_fields")
    def fill_shop_fields(self, name, location, time_zone, industry, traffic):

        self.type_in(self.shop_name_input, name)
        self.type_in(self.shop_location_input, location)
        self.type_in(self.shop_timezone_input, time_zone)
        self.get_elements(self.timezone_list_item, contains_text=time_zone).click()
        self.click(self.shop_industry)
        self.get_elements(self.industry_list_item, contains_text=industry).click()
        self.click(self.shop_traffic)
        self.get_elements(self.traffic_list_item, contains_text=traffic).click()

        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        self.select_time(self.open_hours_start_input, self.open_hours_end_input, apply=True)

        shop_data = [self.get_text(self.shop_name_input, True), self.get_text(self.shop_location_input, True),
                     self.get_text(self.shop_timezone_input, True), self.get_text(self.shop_industry),
                     self.get_text(self.shop_traffic)]
        return shop_data
        # self.select_time(self.open_hours_weekend_start_input, self.open_hours_weekend_end_input, apply=True)

    @allure.step("save shop")
    def save_shop(self):

        self.click(self.save_shop_btn)
        self.check_presence(self.congrats_panel)

    @allure.step("save edit data")
    def save_changes(self):

        self.click(self.save_shop_btn)
        self.check_presence(self.save_changes_label)

    @allure.step("Check congrats panel and accept it")
    def check_congrats_and_apply(self):
        text_on_panel = ('Congratulations!You have added a shop. To start collecting data,'
                         ' you must install and activate sensors.Got it!')
        self.check_presence(self.congrats_panel)
        self.should_be(self.congrats_panel, text_on_panel)
        self.click(self.got_it_btn)

    def check_edit_page_opened(self):
        self.check_presence(self.shop_name_input)

    def check_shop_data(self, shop_data):
        assert self.get_text(self.shop_name_input, True) == shop_data[0]
        assert self.get_text(self.shop_location_input, True) == shop_data[1]
        assert self.get_text(self.shop_timezone_input, True) == shop_data[2]
        assert self.get_text(self.shop_industry) == shop_data[3]
        assert self.get_text(self.shop_traffic) == shop_data[4]
