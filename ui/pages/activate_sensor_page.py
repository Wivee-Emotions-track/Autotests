import allure

from ui.pages.dashboard_page import DashboardPage


class ActivateSensorPage(DashboardPage):

    continue_btn = '.ant-btn-primary'
    check_circle_label = '[aria-label="check"]'
    upload_photo_input = '.ant-upload [type="file"]'
    search_shop_input = '.ant-input-search input'
    shops_list_item = '.ant-space-item'
    setup_sensor_position_btn = '.ant-popover-inner .ant-btn-primary'
    activate_btn = '.ant-btn-primary'

    @allure.step("add sensor")
    def add_sensor(self):
        self.check_presence(self.check_circle_label)
        self.click(self.continue_btn)
        self.check_presence(self.check_circle_label, False)

    @allure.step("upload sensor photo")
    def upload_sensor_photo(self, path_to_photo):
        self.page.set_input_files(self.upload_photo_input, path_to_photo)
        self.click(self.continue_btn)

    @allure.step("search shop")
    def search_shop(self, shop_name):
        self.type_in(self.search_shop_input, shop_name)
        self.click(self.shops_list_item)
        # self.get_elements(self.shops_list_item, contains_text=shop_name).click()

    def continue_flow(self):
        self.click(self.continue_btn)

    def setup_position(self):
        self.check_presence(self.setup_sensor_position_btn)
        self.click(self.setup_sensor_position_btn)

    def activate_sensor(self):
        self.click(self.activate_btn)

    def check_success(self):
        self.check_presence(self.check_circle_label)