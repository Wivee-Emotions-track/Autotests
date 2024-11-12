import random
from datetime import datetime, timedelta
from time import sleep

import allure

from ui.locators.analytics_page_locators import AnalyticsPageLocators
from ui.pages.base_page import BasePage

filename = 'DataAnalytics-2024-07-03-2024-07-15'


class AnalyticsPage(BasePage):

    graphics_btn = '[data-icon="line-chart"]'
    table_btn = '[data-icon="table"]'

    export_btn = '.ant-flex-justify-space-between .ant-btn-primary'
    export_file_name_input = '[id="report-settings_fileName"]'

    # settings
    settings_btn = '[data-icon="setting"]'
    settings_form = '.ant-drawer-content'
    switchers_list = '.ant-drawer-content .ant-space'
    switcher = '[role="switch"]'
    save_btn = '//span[text()="Save"]'

    # table
    column_sorter = '.ant-table-column-sorters'
    comparison_dropdown = '.ant-space .ant-dropdown-trigger'
    comparison_menu_item = '.ant-dropdown-menu-item'
    cell = '.ant-table-cell'

    # date filter
    filter_days_ago = '//div[contains(@class, "ant-picker-presets")]//li'
    start_date_input = '[placeholder="Start date"]'
    end_date_input = '[placeholder="End date"]'

    # time filter
    start_time_input = '[placeholder="Start Time"]'
    end_time_input = '[placeholder="End Time"]'
    hours_items_list = '[data-type="hour"] .ant-picker-time-panel-cell'
    minutes_items_list = '[data-type="minute"] .ant-picker-time-panel-cell'

    chart_label = '.plot-container'
    download_btn = '[type="submit"]'
    download_form = '.ant-modal-content'

    @allure.step("open_chart")
    def open_graphics(self):
        self.click(self.graphics_btn)
        self.check_presence(self.chart_label)

    def check_page_opened(self):
        self.check_presence(self.cell)

    @allure.step("open_table")
    def open_table(self):
        self.click(self.table_btn)
        self.check_presence(self.cell)

    @allure.step("open_settings")
    def open_settings(self):
        self.click(self.settings_btn)
        self.check_presence(self.settings_form)

    @allure.step("export data")
    def export_data(self, file_name):
        self.click(self.export_btn)
        self.check_presence(self.download_form)
        self.type_in(self.export_file_name_input, file_name)
        self.click(self.download_btn)
        self.check_presence(self.export_file_name_input, visible=False)

    @allure.step("switch column presence")
    def switch_menu_column(self, column_name: str):
        element = self.get_elements(self.switchers_list, column_name)
        switcher = self.get_child_element(element, self.switcher)
        switcher.click()

    @allure.step("save table settings")
    def save_settings(self):
        self.click(self.save_btn)
        self.check_presence(self.settings_form)

    @allure.step("check_column_presence after settings changing")
    def check_column_presence(self, column_name, presence=False):
        column = self.get_elements(self.column_sorter, column_name)
        if not presence:
            assert column is None, f'Column with name {column_name} should not be displayed'
        else:
            assert column is not None, f'Column with name {column_name} should be displayed'

    @allure.step("Select comparison type")
    def select_comparison(self, comparison_type):
        self.check_presence(self.cell)
        self.click(self.comparison_dropdown)
        comparyson = self.get_elements(self.comparison_menu_item, comparison_type)
        comparyson.click()

    @allure.step("check_comparison_module_is_active")
    def check_comparison_module_is_active(self):

        self.check_presence(self.cell)
        cell = self.get_elements(self.cell, index=15)
        assert "%" in cell.text_content(), 'Compare module wasn`t added'

    @allure.step("select days ago param in filter")
    def select_days_ago_in_filter(self, days_ago: str):
        self.check_presence(self.cell)
        self.click(self.start_date_input)
        self.check_presence(self.filter_days_ago)
        self.get_elements(self.filter_days_ago, contains_text=days_ago).click()

    @allure.step("check date in filters with days ago option")
    def check_date_in_filter(self, days_ago: int):

        # Получаем текущую дату
        today = datetime.today()
        end_date = self.get_text(self.end_date_input, input=True)
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        # Сравниваем текущую дату и дату окончания фильтрации
        assert end_date_obj.date() == today.date(), (f'End date {end_date} is not corresponding'
                                                     f' with current date {today.date()}')

        # Вычисляем дату n дней назад
        days_ago_date = today - timedelta(days=days_ago)

        start_date = self.get_text(self.start_date_input, input=True)
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

        # Сравниваем полученную дату с ожидаемой
        assert start_date_obj.date() == days_ago_date.date(), (f'Start date {start_date} is not corresponding with'
                                                               f' current date {today.date()} - {days_ago} days')

    @allure.step("check_date_in_filter_with_previous_week")
    def check_date_in_filter_with_previous_week(self):

        sunday = self.get_text(self.start_date_input, input=True)
        saturday = self.get_text(self.end_date_input, input=True)
        sunday_date = datetime.strptime(sunday, '%Y-%m-%d').date()
        saturday_date = datetime.strptime(saturday, '%Y-%m-%d').date()

        today = datetime.today()
        current_weekday = today.weekday()

        # Находим последнее воскресенье и предыдущий понедельник
        last_saturday = today - timedelta(days=current_weekday + 2)
        last_sunday = last_saturday - timedelta(days=6)

        assert sunday_date == last_sunday.date(), (f'Sunday date {sunday_date} is not corresponding with'
                                                   f' calculated date {last_sunday.date()}')

        assert saturday_date == last_saturday.date(), (f'Saturday date {saturday_date} is not corresponding with'
                                                       f' calculated date {last_saturday.date()}')

    @allure.step("check_date_in_filter_with_previous_month")
    def check_date_in_filter_with_previous_month(self):

        first_day_of_month = self.get_text(self.start_date_input, input=True)
        last_day_of_month = self.get_text(self.end_date_input, input=True)

        current_date = datetime.now()

        # Вычисляем начало и конец прошлого месяца
        if current_date.month == 1:
            start_of_last_month = datetime(current_date.year - 1, 12, 1)
        else:
            start_of_last_month = datetime(current_date.year, current_date.month - 1, 1)

        # Конец прошлого месяца — это последний день предыдущего месяца
        end_of_last_month = start_of_last_month.replace(day=1) + timedelta(days=31)
        end_of_last_month = end_of_last_month.replace(day=1) - timedelta(days=1)

        start_of_last_month_str = start_of_last_month.strftime('%Y-%m-%d')
        end_of_last_month_str = end_of_last_month.strftime('%Y-%m-%d')

        assert first_day_of_month == start_of_last_month_str, (f'First date of the month {first_day_of_month}'
                                                               f' is not corresponding with'
                                                               f' calculated date {start_of_last_month_str}')

        assert last_day_of_month == end_of_last_month_str, (f'Last date of the month {last_day_of_month}'
                                                            f' is not corresponding with'
                                                            f' calculated date {end_of_last_month_str}')

    def select_time(self):
        start_time = []
        end_time = []
        self.check_presence(self.cell)
        self.click(self.start_time_input)
        self.check_presence(self.hours_items_list)
        hours_list_items = self.get_elements(self.hours_items_list)
        minutes_list_items = self.get_elements(self.minutes_items_list)

        begin_hour_element = random.choice(hours_list_items[:-1])
        begin_minute_element = random.choice(minutes_list_items[:-1])
        start_time.append(begin_hour_element.text_content())
        start_time.append(begin_minute_element.text_content())

        begin_hour_element.click()
        begin_minute_element.click()

        begin_hour_element_index = hours_list_items.index(begin_hour_element)
        begin_minute_element_index = minutes_list_items.index(begin_minute_element)

        end_hour_element = (
            hours_list_items)[begin_hour_element_index + 1]
        end_minute_element = (
            minutes_list_items)[begin_minute_element_index + 1]

        self.click(self.end_time_input)
        end_time.append(end_hour_element.text_content())
        end_time.append(end_minute_element.text_content())
        end_hour_element.click()
        end_minute_element.click()

        return start_time, end_time

    def check_time_filer(self, start_time: list, end_time: list):
        assert start_time[0], start_time[1] in self.get_text(self.start_time_input)
        assert end_time[0], end_time[1] in self.get_text(self.end_time_input)
