import allure

from ui.pages.dashboard_page import DashboardPage


class OpenedShopPage(DashboardPage):

    shop_plan_label = '.ant-card'

    @allure.step("check shop page opened")
    def check_shop_opened(self):
        self.check_presence(self.shop_plan_label)
