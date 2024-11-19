import time
from datetime import datetime
from os import path

import allure
import pytest

from ui.pages.create_shop_page import CreateShopPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.shop_page import OpenedShopPage
from ui.pages.shops_page import ShopsPage


@pytest.fixture()
def create_shop(fixture_shops_api):
    shop_name = f'AutotestShop_{datetime.utcnow().strftime("%d_%m_%H_%M")}'
    shop_id = fixture_shops_api.create_shop(path.join(path.dirname(__file__), 'test_data', 'plan.PNG'),
                                            shop_name=shop_name, location='Poland',
                                            timezone='Poland', industry='Apparel and Fashion',
                                            traffic="10 per day")
    yield shop_name


@allure.title("Test shop setup")
def test_shop_setup(page, login):
    shop_name = f'AutotestShop_{datetime.utcnow().strftime("%d_%m_%H_%M")}'
    shops_page = ShopsPage(page)
    time.sleep(5) # todo
    shops_page.add_shop()

    create_shop = CreateShopPage(page)
    create_shop.upload_plan(path.join(path.dirname(__file__), 'test_data', 'plan.PNG'))
    create_shop.go_to_shop_details()
    create_shop.fill_shop_fields(shop_name, "Poland", "Poland", "Automotive", "10 per Day")
    create_shop.save_shop()
    create_shop.check_congrats_and_apply()
    time.sleep(5) # todo
    shops_page.search_shop(shop_name)
    assert shops_page.get_elements(shops_page.table_row, contains_text=shop_name), f'Row with shop {shop_name} is not displayed'

@allure.title("Test edit shop")
def test_edit_shop(page, create_shop, login):
    shop_name = create_shop
    shop_new_name = f'AutotestShop_{datetime.utcnow().strftime("%d_%m_%H_%M")}'
    sidebar = DashboardPage(page)
    sidebar.open_shops_page()
    shops_page = ShopsPage(page)
    shops_page.search_shop(shop_name)
    shops_page.edit_shop()

    create_shop = CreateShopPage(page)
    create_shop.check_edit_page_opened()
    shop_data = create_shop.fill_shop_fields(shop_new_name, "Dublin", "Dublin",
                                             "Electronics", "50 per Day")
    create_shop.save_changes()
    create_shop.page.go_back()

    shops_page.search_shop(shop_new_name)
    shops_page.edit_shop()
    create_shop.check_edit_page_opened()
    create_shop.check_shop_data(shop_data)


@allure.title("Test open shop")
def test_open_shop(page, create_shop, login):
    shop_name = create_shop
    sidebar = DashboardPage(page)
    sidebar.open_shops_page()
    shops_page = ShopsPage(page)
    shops_page.search_shop(shop_name)
    shops_page.open_shop(shop_name)

    opened_shops = OpenedShopPage(page)
    opened_shops.check_shop_opened()
