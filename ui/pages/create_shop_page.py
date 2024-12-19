import os
import time
from time import sleep

import allure

from configs.project_paths import SCREENSHOTS_PATH
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage


class CreateShopPage(DashboardPage):

    upload_plan_input = '.ant-upload input'
    uploaded_plan = '.konvajs-content'
    continue_btn = '.ant-btn-primary'
    edit_zones_tab = '[aria-controls="rc-tabs-0-panel-zones"]'
    edit_info_tab = '[aria-controls="rc-tabs-0-panel-meta"]'

    shop_name_input = '[id="name"]'
    shop_location_input = '[id="location"]'
    shop_timezone_input = '[id="timeZone"]'
    shop_timezone_label = '//input[@id="timeZone"]/..//following-sibling::span'
    shop_industry_label = '//input[@id="industry"]/..//following-sibling::span'
    shop_traffic_label = '//input[@id="traffic"]/..//following-sibling::span'

    timezone_list_item = '.ant-select-item'
    shop_industry = '[id="industry"]'
    industry_list_item = '.ant-select-item'
    shop_traffic = '[id="traffic"]'
    traffic_list_item = '.ant-select-item'
    congrats_panel = '.ant-modal-content'
    got_it_btn = '.ant-modal-content .ant-btn-primary'
    save_changes_label = '[aria-label="check-circle"]'

    # edit zones
    zones_items_list = '[id="rc-tabs-0-panel-zones"] .ant-typography-ellipsis-single-line'

    # open hours
    open_hours_start_input = '[id="openHours"]'
    open_hours_end_input = '//input[@id="openHours"]/..//following-sibling::div/input'
    open_hours_weekend_start_input = '[id="openHoursWeekend"]'
    open_hours_weekend_end_input = '//input[@id="openHoursWeekend"]/..//following-sibling::div/input'
    save_shop_btn = '[type="submit"]'
    save_zone_btn = '[aria-labelledby="rc-tabs-0-tab-zones"] .ant-btn-primary'

    # edit zones
    zones_list_btn = '.ant-tabs-content .ant-flex button'

    @allure.step("upload plan")
    def upload_plan(self, path_to_plan):
        self.page.set_input_files(self.upload_plan_input, path_to_plan)
        self.check_presence(self.uploaded_plan)

    @allure.step('draw zone')
    def draw_zone(self, x=50, y=25, screenshot_name='canvas_screenshot.png'):
        canvas_box = self.page.locator(self.uploaded_plan).bounding_box()

        # Координаты начала прямоугольника (центр canvas)
        start_x = canvas_box["x"] + canvas_box["width"] / 2 - x
        start_y = canvas_box["y"] + canvas_box["height"] / 2 - y

        # Координаты конца прямоугольника
        end_x = canvas_box["x"] + canvas_box["width"] / 2 + x
        end_y = canvas_box["y"] + canvas_box["height"] / 2 + y

        self.page.mouse.move(start_x, start_y)  # Переместить мышь к начальной точке
        self.page.mouse.down()                  # Зажать левую кнопку мыши
        self.page.mouse.move(end_x, end_y)      # Перетащить мышь к конечной точке
        self.page.mouse.up()

        canvas_box = self.page.locator(self.uploaded_plan)
        screenshot_path = os.path.join(SCREENSHOTS_PATH, screenshot_name)
        canvas_box.screenshot(path=screenshot_path)
        return screenshot_path

    @allure.step('drag zone')
    def drag_zone_via_coordinates(self, x2, y2, x1=0, y1=0, screenshot_name='drag_screenshot.png'):

        canvas_box = self.page.locator(self.uploaded_plan).bounding_box()

        # Координаты начала прямоугольника (центр canvas)
        start_x = canvas_box["x"] + canvas_box["width"] / 2 - x1
        start_y = canvas_box["y"] + canvas_box["height"] / 2 - y1

        # Координаты конца прямоугольника
        end_x = canvas_box["x"] + canvas_box["width"] / 2 + x2
        end_y = canvas_box["y"] + canvas_box["height"] / 2 + y2

        self.page.mouse.click(start_x, start_y)  # Переместить мышь к начальной точке
        self.page.mouse.down()  # Зажать левую кнопку мыши
        self.page.mouse.move(end_x, end_y)  # Перетащить мышь к конечной точке
        self.page.mouse.up()

        canvas_box = self.page.locator(self.uploaded_plan)
        screenshot_path = os.path.join(SCREENSHOTS_PATH, screenshot_name)
        canvas_box.screenshot(path=screenshot_path)
        return screenshot_path

    @allure.step('remove zone')
    def remove_zone_via_coordinates(self, x2, y2, x1=0, y1=0):

        canvas_box = self.page.locator(self.uploaded_plan).bounding_box()

        # Координаты начала прямоугольника (центр canvas)
        start_x = canvas_box["x"] + canvas_box["width"] / 2 - x1
        start_y = canvas_box["y"] + canvas_box["height"] / 2 - y1

        self.page.mouse.click(start_x, start_y)  # Переместить мышь к начальной точке

        canvas_box = self.page.locator(self.uploaded_plan)
        screenshot_path = os.path.join(SCREENSHOTS_PATH, 'drag_screenshot.png')
        canvas_box.screenshot(path=screenshot_path)
        return screenshot_path

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
    def save_shop(self, check_congrats=True):

        self.click(self.save_shop_btn)
        if check_congrats:
            self.check_presence(self.congrats_panel)

    @allure.step("save zone")
    def save_zone(self):

        self.click(self.save_zone_btn)

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
        assert self.get_text(self.shop_name_input, True) == shop_data[0],\
            (f'Field that contains text - {self.get_text(self.shop_name_input, True)},'
             f' is not equal reference {shop_data[0]}')

        assert self.get_text(self.shop_location_input, True) == shop_data[1],\
            (f'Field that contains text - {self.get_text(self.shop_location_input, True)},'
             f' is not equal reference {shop_data[1]}')

        assert self.get_text(self.shop_timezone_label, attribute='title') == shop_data[2],\
            (f'Field that contains text - {self.get_text(self.shop_timezone_label, attribute="title")},'
             f' is not equal reference {shop_data[2]}')

        assert self.get_text(self.shop_industry_label, attribute="title") == shop_data[3],\
            (f'Field that contains text - {self.get_text(self.shop_industry_label, attribute="title")},'
             f' is not equal reference {shop_data[3]}')

        assert self.get_text(self.shop_traffic_label, attribute="title") == shop_data[4],\
            (f'Field that contains text - {self.get_text(self.shop_traffic_label, attribute="title")},'
             f' is not equal reference {shop_data[4]}')

    def go_to_edit_zone_tab(self):
        self.click(self.edit_zones_tab)
        self.check_presence(self.zones_items_list)

    def go_to_edit_info_tab(self):
        self.click(self.edit_info_tab)
        self.check_presence(self.save_shop_btn)

    def select_zone(self, zone_name):
        zone = self.get_elements(self.zones_items_list, zone_name)
        zone.click()

