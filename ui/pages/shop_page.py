import allure

from ui.pages.dashboard_page import DashboardPage


class OpenedShopPage(DashboardPage):

    shop_plan_label = '.ant-card'
    zone_info_label = '.ant-popover'


    @allure.step("check shop page opened")
    def check_shop_opened(self):
        self.check_presence(self.shop_plan_label)

    @allure.step("check zone info")
    def check_zone_info(self, zone_name, sensor_mac, sensor_status):

        self.should_be(self.zone_info_label, contains_text=zone_name)
        self.should_be(self.zone_info_label, contains_text=sensor_mac)
        self.should_be(self.zone_info_label, contains_text=sensor_status)
