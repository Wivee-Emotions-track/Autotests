import random
import time
from datetime import datetime, timedelta
import allure

from ui.pages.dashboard_page import DashboardPage


class AnalyticsPage(DashboardPage):

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
    table_row = '.ant-table-row'

    # date filter
    filter_days_ago = '//div[contains(@class, "ant-picker-presets")]//li'
    start_date_input = '[placeholder="Start date"]'
    end_date_input = '[placeholder="End date"]'

    # Zones and shops filter
    zones_filter = '//span[text()="Zones"]'
    zones_list_item = '.ant-select-tree-node-content-wrapper'
    shops_filter = '//span[text()="Shops"]'
    shops_list_item = '.ant-select-tree-node-content-wrapper'
    search_filter_input = '[placeholder="Search by name"]'

    # time filter
    start_time_input = '[placeholder="Start Time"]'
    end_time_input = '[placeholder="End Time"]'
    hours_items_list = '[data-type="hour"] .ant-picker-time-panel-cell'
    minutes_items_list = '[data-type="minute"] .ant-picker-time-panel-cell'

    # chart
    first_filter = '(//div/span[contains(@class, "ant-select-selection-item")])[1]'
    second_filter = '(//div/span[contains(@class, "ant-select-selection-item")])[2]'
    chart_filter_items = '.ant-select-item'
    chart_filter = '.ant-select-selection-item'
    legend_label = '//*[@class="legendtext"]'
    options_list_item = '.ant-segmented-item'

    chart_label = '.plot-container'
    download_btn = '[type="submit"]'
    download_form = '.ant-modal-content'

    @allure.step("open_chart_and_check")
    def open_graphics(self):
        self.click(self.graphics_btn)
        self.check_presence(self.chart_label)

    def check_page_opened(self):
        self.check_presence(self.export_btn)

    @allure.step("open_table_and_check")
    def open_table(self):
        self.click(self.table_btn)
        self.check_presence(self.cell)

    @allure.step("open_settings_and_check")
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
        for cell_number in range(30):
            cell = self.get_elements(self.cell, index=cell_number)
            if "%" in cell.text_content():
                break
        else:
            raise (Exception('Compare module wasn`t added'))

    @allure.step("select days ago param in filter")
    def select_days_ago_in_filter(self, days_ago: str):
        self.check_page_opened()
        self.click(self.start_date_input)
        self.check_presence(self.filter_days_ago)
        self.get_elements(self.filter_days_ago, contains_text=days_ago).click()

    @allure.step("check date in filters with days ago option")
    def check_date_in_filter(self, days_ago: int):

        # Получаем текущую дату
        self.check_presence(self.loader_label, False)
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

        self.check_presence(self.loader_label, False)
        time.sleep(5)  # todo
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

        self.check_presence(self.loader_label, False)
        time.sleep(5)  # todo
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

    @allure.step("Check time filter")
    def check_time_filer(self, start_time: list, end_time: list):
        assert start_time[0], start_time[1] in self.get_text(self.start_time_input)
        assert end_time[0], end_time[1] in self.get_text(self.end_time_input)

    @allure.step("Select zones filter")
    def select_zones(self, zone_name):

        self.click(self.zones_filter)
        self.check_presence(self.zones_list_item)
        self.get_elements(self.zones_list_item, zone_name).click()
        self.click(self.dashboard_title)

    @allure.step("Select shops filter")
    def select_shops(self, shop_name):

        self.click(self.shops_filter)
        self.type_in(self.search_filter_input, shop_name)
        self.check_presence(self.shops_list_item)
        self.get_elements(self.shops_list_item, shop_name).click()
        self.click(self.dashboard_title)

    @allure.step("Check table with zone or shop filter")
    def check_table_with_filters(self, shop_name):
        self.check_presence(self.table_row)
        assert self.get_elements(self.table_row, contains_text=shop_name), (f'Shop {shop_name}'
                                                                            f'doesn`t display in table with filter')

    @allure.step("Select_chart_option")
    def select_chart_option(self, option_name: str):

        self.get_elements(self.options_list_item, option_name).click()

    @allure.step("Check_legends_containing")
    def check_legends_containing(self, legend_number, legend_data):
        self.check_presence(self.legend_label)
        legend = self.get_elements(self.legend_label, index=legend_number)

        for legend_text in legend_data:
            assert legend_text in legend.text_content(), 'Data in legend is not valid'

    @allure.step("Check table cells is not empty")
    def check_table_is_not_empty(self, shops):
        self.check_presence(self.table_row)
        time.sleep(2) # todo
        for shop_name in shops:
            row = self.get_elements(self.table_row, contains_text=shop_name)
            cells = self.get_childs_element(row, self.cell)[1:]
            for cell in cells:
                assert cell.text_content() != '', f'No data for shop {shop_name}'

    def add_chart_filter(self, filter_name):
        self.click(self.chart_filter)
        self.get_elements(self.chart_filter_items, contains_text=filter_name).click()
