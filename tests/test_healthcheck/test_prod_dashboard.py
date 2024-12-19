import allure
import pytest

from ui.pages.analytics_page import AnalyticsPage
from ui.pages.shops_page import ShopsPage
from ui.pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username, shops", [('lenskart', ['Lenskart at Mylapore, Chennaj', 'Total']),
                        ('iroha', ['IROHA_NEW', 'Total']),
                        ('demo', ['Wayvee XL', 'Wayvee M', 'Wayvee XS'])
                        ])
@allure.title("Test for checking data in analytic table")
def test_analytic_table_check_data(page, get_config, username, shops):

    login_page = LoginPage(page, get_config['urls']['host'])
    login_page.open('https://app.wayvee.com/analytics')
    # login_page.open()
    login_page.login(get_config['credentials'][username]['login'], get_config['credentials'][username]['login'])
    analytics_page = AnalyticsPage(page)
    analytics_page.check_page_opened()
    analytics_page.check_loader_absence()
    analytics_page.check_table_is_not_empty(shops)


@pytest.mark.parametrize(
    "username, shops", [('lenskart', ['Lenskart at Mylapore, Chennaj']),
                        ('iroha', ['IROHA', 'IROHA_NEW']),
                        ('demo', ['Wayvee XL', 'Wayvee M', 'Wayvee XS'])
                        ])
@allure.title("Test for checking data in shop table")
def test_shop_table_check_data(page, get_config, username, shops):

    login_page = LoginPage(page, get_config['urls']['host'])
    # login_page.open('https://app.wayvee.com/shops')
    login_page.open(get_config['urls']['host'] + '/shops')
    login_page.login(get_config['credentials'][username]['login'], get_config['credentials'][username]['login'])
    shops_page = ShopsPage(page)
    shops_page.check_loader_absence()
    shops_page.check_page_opened()
    shops_page.check_table_is_not_empty(shops)
