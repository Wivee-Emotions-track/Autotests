import time
from datetime import datetime

import allure
import pytest
from ui.pages.login_page import LoginPage
from ui.pages.analytics_page import AnalyticsPage


@pytest.fixture(scope="function")
def login_with_date(page, get_config):
    username = get_config['credentials']['super_user']['login']
    password = get_config['credentials']['super_user']['password']

    login_page = LoginPage(page, get_config['urls']['host'])
    url_with_date_filters = login_page.url + '/analytics?zones=&shops=&from=2023-08-13&to=2024-11-11'
    login_page.open(url_with_date_filters)
    login_page.login(username, password)
    analytics_page = AnalyticsPage(page)
    analytics_page.check_page_opened()


@allure.title("Test table preview")
def test_table_check(page, login_with_date):
    file_name = f'AutotestExport_{datetime.utcnow().strftime("%d_%m_%H_%M")}'
    analytics_page = AnalyticsPage(page)
    analytics_page.open_graphics()
    analytics_page.open_table()
    analytics_page.open_settings()
    analytics_page.export_data(file_name)


@allure.title("Test edit table columns")
def test_edit_table_columns(page, login_with_date):
    analytics_page = AnalyticsPage(page)
    analytics_page.check_page_opened()
    analytics_page.open_settings()

    with allure.step("Hide columns"):
        analytics_page.switch_menu_column('Avg. Dwell Time')
        analytics_page.switch_menu_column('Dwell Number')
        analytics_page.switch_menu_column('Engagements Number')
        analytics_page.switch_menu_column('Avg. Engagements per Customer')
        analytics_page.switch_menu_column('Avg. Speed')
        analytics_page.switch_menu_column('C-SAT')
        analytics_page.switch_menu_column('Bypassers Number')

    analytics_page.save_settings()

    analytics_page.check_column_presence('Avg. Dwell Time')
    analytics_page.check_column_presence('Dwell Number')
    analytics_page.check_column_presence('Engagements Number')
    analytics_page.check_column_presence('Avg. Engagements per Customer')
    analytics_page.check_column_presence('Avg. Speed')
    analytics_page.check_column_presence('C-SAT')
    analytics_page.check_column_presence('Bypassers Number')


@allure.title("Test check filters")
def test_edit_table(page, login_with_date):
    analytics_page = AnalyticsPage(page)
    analytics_page.select_comparison('Preceding Period')
    analytics_page.click(analytics_page.table_btn)  # to close drop down menu
    time.sleep(3) # todo
    analytics_page.check_comparison_module_is_active()


@allure.title("Test check date filters")
def test_date_filter(page, login):

    analytics_page = AnalyticsPage(page)
    analytics_page.check_page_opened()
    analytics_page.select_days_ago_in_filter('Last 90 Days')
    analytics_page.check_date_in_filter(days_ago=90)

    analytics_page.select_days_ago_in_filter('Last Week')
    analytics_page.check_date_in_filter_with_previous_week()

    analytics_page.select_days_ago_in_filter('Last Month')
    analytics_page.check_date_in_filter_with_previous_month()


@allure.title("Test check time filter")
def test_time_filter(page, login):

    analytics_page = AnalyticsPage(page)
    analytics_page.check_page_opened()
    time = analytics_page.select_time(analytics_page.start_time_input, analytics_page.end_time_input)
    analytics_page.check_time_filer(time[0], time[1])


@allure.title("Test check zones filter")
def test_zones_filter(page, login_with_date):

    analytics_page = AnalyticsPage(page)
    analytics_page.select_zones('TV')
    analytics_page.check_table_with_filters('Auki Labs ( final )')


@allure.title("Test check shops filter")
def test_shops_filter(page, login_with_date):

    analytics_page = AnalyticsPage(page)
    analytics_page.select_shops('Auki Labs ( final )')
    analytics_page.check_table_with_filters('Auki Labs ( final )')


@allure.title("Test check charts filter")
def test_charts_filter(page, login_with_date):

    analytics_page = AnalyticsPage(page)
    analytics_page.check_page_opened()
    analytics_page.open_graphics()
    analytics_page.select_zones("TV")
    analytics_page.select_chart_option('Overall')
    analytics_page.check_legends_containing(legend_number=0, legend_data=["Dwell Number"])
    analytics_page.check_legends_containing(legend_number=1, legend_data=["Bypassers Number"])

    analytics_page.select_chart_option('Data Source')
    analytics_page.check_legends_containing(legend_number=0, legend_data=["Dwell Number", "RadarRawDataProcessor"])
    analytics_page.check_legends_containing(legend_number=1, legend_data=["Bypassers Number", "RadarRawDataProcessor"])

    analytics_page.select_chart_option('Zone')
    analytics_page.check_legends_containing(legend_number=0, legend_data=["Dwell Number", "TV"])
    analytics_page.check_legends_containing(legend_number=1, legend_data=["Bypassers Number", "TV"])

    analytics_page.select_chart_option('Shop')
    analytics_page.check_legends_containing(legend_number=0, legend_data=["Dwell Number", "Auki Labs ( final )"])
    analytics_page.check_legends_containing(legend_number=1, legend_data=["Bypassers Number", "Auki Labs ( final )"])

