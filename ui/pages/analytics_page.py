from time import sleep
from playwright.sync_api import Page
from configs.config import BASE_URL
from ui.locators.analytics_page_locators import AnalyticsPageLocators

filename = 'DataAnalytics-2024-07-03-2024-07-15'
class AnalyticsPage:
    def __init__(self, page: Page):
        self.page = page

    def click_table(self):
        self.page.click(AnalyticsPageLocators.TABLE_BUTTON)
        self.page.wait_for_load_state()
        #self.page.goto(f"{BASE_URL}/analytics")
        sleep(2)

    def click_graphics(self):
        self.page.click(AnalyticsPageLocators.LINE_CHART_BUTTON)
        sleep(2)

    def click_edit_table(self):
        self.page.get_by_text(AnalyticsPageLocators.EDIT_TABLE_BUTTON).click()
        sleep(2)

    def click_export(self):
        self.page.click(AnalyticsPageLocators.EXPORT_BUTTON)
        sleep(2)

    def click_download(self, filename: str = "default") -> object:
        self.page.fill(AnalyticsPageLocators.FILE_NAME_INPUT, filename)
        self.page.click(AnalyticsPageLocators.DOWNLOAD_BUTTON)
        sleep(2)

    def open(self):
        self.page.goto(BASE_URL)
