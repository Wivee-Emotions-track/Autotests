import allure
import pytest

from ui.pages.analytics_page import AnalyticsPage
from ui.pages.shops_page import ShopsPage
from ui.pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username, password, shops", [('test-lenskart@srv1.mail-tester.com', 'test-lenskart@srv1.mail-tester.com',
                                   ['Lenskart at Mylapore, Chennaj', 'Total']),
                                  ('test-IRONA@srv1.mail-tester.com', 'test-IRONA@srv1.mail-tester.com',
                                   ['IROHA_NEW', 'Total']),
                                  ('test-demo@srv1.mail-tester.com', 'test-demo@srv1.mail-tester.com',
                                   ['Wayvee XL', 'Wayvee M', 'Wayvee XS'])
                                  ])
@allure.title("Test for checking data in analytic table")
def test_analytic_table_check_data(page, username, password, shops):

    login_page = LoginPage(page)
    login_page.open('https://app.wayvee.com/analytics')
    login_page.login(username, password)
    analytics_page = AnalyticsPage(page)
    analytics_page.check_page_opened()
    analytics_page.check_loader_absence()
    analytics_page.check_table_is_not_empty(shops)


@pytest.mark.parametrize(
    "username, password, shops", [('test-lenskart@srv1.mail-tester.com', 'test-lenskart@srv1.mail-tester.com',
                                   ['Lenskart at Mylapore, Chennaj']),
                                  ('test-IRONA@srv1.mail-tester.com', 'test-IRONA@srv1.mail-tester.com',
                                   ['IROHA', 'IROHA_NEW']),
                                  ('test-demo@srv1.mail-tester.com', 'test-demo@srv1.mail-tester.com',
                                   ['Wayvee XL', 'Wayvee M', 'Wayvee XS'])
                                  ])
@allure.title("Test for checking data in shop table")
def test_shop_table_check_data(page, username, password, shops):

    login_page = LoginPage(page)
    login_page.open('https://app.wayvee.com/shops')
    login_page.login(username, password)
    shops_page = ShopsPage(page)
    shops_page.check_loader_absence()
    shops_page.check_page_opened()
    shops_page.check_table_is_not_empty(shops)
