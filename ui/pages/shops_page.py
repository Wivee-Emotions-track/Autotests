from ui.pages.dashboard_page import DashboardPage


class ShopsPage(DashboardPage):

    add_shop_btn = '.ant-row .ant-btn-icon'

    def add_shop(self):
        self.click(self.add_shop_btn)
        self.check_presence(self.add_shop_btn, visible=False)
