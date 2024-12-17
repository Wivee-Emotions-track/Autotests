import os
import time
from datetime import datetime
from os import path

import allure
import pytest

from configs.project_paths import SCREENSHOTS_PATH
from helpers.images_compare import compare_image
from ui.pages.activate_sensor_page import ActivateSensorPage
from ui.pages.create_shop_page import CreateShopPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.shop_page import OpenedShopPage
from ui.pages.shops_page import ShopsPage


@pytest.fixture()
def create_shop(fixture_shops_api):
    shop_name = f'AutotestShop_{datetime.utcnow().strftime("%d_%m_%H_%M_%S")}'
    shop_id = fixture_shops_api.create_shop(path.join(path.dirname(__file__), 'test_data', 'plan.PNG'),
                                            shop_name=shop_name, location='Poland',
                                            timezone='Poland', industry='Apparel and Fashion',
                                            traffic="10 per day")
    yield shop_name


@pytest.fixture()
def create_shop_via_ui(page, login):
    shop_name = f'AutotestShop_{datetime.utcnow().strftime("%d_%m_%H_%M_%S")}'
    shops_page = ShopsPage(page)
    time.sleep(5)  # todo
    shops_page.add_shop()

    create_shop = CreateShopPage(page)
    create_shop.upload_plan(path.join(path.dirname(__file__), 'test_data', 'test_shop_setup', 'plan.PNG'))
    create_shop.draw_zone()
    create_shop.go_to_shop_details()
    create_shop.fill_shop_fields(shop_name, "Poland", "Poland", "Automotive", "10 per Day")
    create_shop.save_shop()
    create_shop.check_congrats_and_apply()
    yield shop_name


@allure.title("Test shop setup")
def test_shop_setup(page, login, get_config):

    path_to_reference = path.join(path.dirname(__file__), 'test_data', 'test_shop_setup', 'canvas_screenshot.PNG')
    shop_name = f'AutotestShop_{datetime.utcnow().strftime("%d_%m_%H_%M_%S")}'
    shops_page = ShopsPage(page)
    time.sleep(5)  # todo
    shops_page.add_shop()

    create_shop = CreateShopPage(page)
    create_shop.upload_plan(path.join(path.dirname(__file__), 'test_data', 'test_shop_setup', 'plan.PNG'))
    path_to_image = create_shop.draw_zone()
    create_shop.go_to_shop_details()
    create_shop.fill_shop_fields(shop_name, "Poland", "Poland", "Automotive", "10 per Day")
    create_shop.save_shop()
    create_shop.check_congrats_and_apply()
    time.sleep(5)  # todo
    shops_page.search_shop(shop_name)
    shops_page.check_search_result(shop_name)
    shops_page.edit_shop()
    create_shop.check_edit_page_opened()
    assert compare_image(path_to_image, path_to_reference), 'Zones on plans are different'
    create_shop.check_shop_data([shop_name, "Poland", "Poland", "Automotive", "10 per Day"])


@allure.title("Test edit shop data")
def test_edit_shop_data(page, create_shop, login):
    shop_name = create_shop
    shop_new_name = f'AutotestShop_{datetime.utcnow().strftime("%d_%m_%H_%M_%S")}'
    sidebar = DashboardPage(page)
    sidebar.open_shops_page()
    shops_page = ShopsPage(page)
    shops_page.search_shop(shop_name)
    shops_page.check_search_result(shop_name)
    shops_page.edit_shop()

    create_shop = CreateShopPage(page)
    create_shop.check_edit_page_opened()
    shop_data = create_shop.fill_shop_fields(shop_new_name, "Dublin", "Dublin",
                                             "Electronics", "50 per Day")
    create_shop.save_changes()
    create_shop.page.go_back()

    shops_page.search_shop(shop_new_name)
    shops_page.check_search_result(shop_new_name)
    shops_page.edit_shop()
    create_shop.check_edit_page_opened()
    create_shop.check_shop_data(shop_data)


@allure.title("Test edit shop add new zone")
def test_edit_shop_add_new_zone(page, create_shop_via_ui):

    screenshot_name = f'ZoneScreen_{datetime.utcnow().strftime("%d_%m_%H_%M_%S")}.PNG'
    path_to_reference = path.join(path.dirname(__file__), 'test_data', 'test_edit_shop_add_new_zone',
                                  'edit_zone_new_zone.PNG')

    shop_name = create_shop_via_ui
    sidebar = DashboardPage(page)
    sidebar.open_shops_page()
    shops_page = ShopsPage(page)
    shops_page.search_shop(shop_name)
    shops_page.check_search_result(shop_name)
    shops_page.edit_shop()
    create_shop = CreateShopPage(page)
    create_shop.go_to_edit_zone_tab()
    time.sleep(15)  # долго подгружается картинка todo

    create_shop.select_zone('Chips')
    path_to_image = create_shop.draw_zone(100, 75, screenshot_name)
    create_shop.save_zone()
    create_shop.page.go_back()

    time.sleep(5)  # todo
    # shops_page.search_shop(shop_name)
    # shops_page.check_search_result(shop_name)
    shops_page.edit_shop()
    create_shop.check_edit_page_opened()
    assert compare_image(path_to_image, path_to_reference), 'Zones on plans are different'


@allure.title("Test edit shop drag_zone")
def test_edit_shop_drag_zone(page, create_shop_via_ui):
    screenshot_name = f'DragZoneScreen_{datetime.utcnow().strftime("%d_%m_%H_%M_%S")}.PNG'
    path_to_reference = path.join(path.dirname(__file__), 'test_data', 'test_edit_shop_drag_zone',
                                  'drag_zone_screen.PNG')

    shop_name = create_shop_via_ui
    sidebar = DashboardPage(page)
    sidebar.open_shops_page()
    shops_page = ShopsPage(page)
    shops_page.search_shop(shop_name)
    shops_page.check_search_result(shop_name)
    shops_page.edit_shop()
    create_shop = CreateShopPage(page)
    create_shop.go_to_edit_zone_tab()
    time.sleep(15)  # долго подгружается картинка todo
    path_to_image = create_shop.drag_zone_via_coordinates(250, 125, screenshot_name=screenshot_name)

    create_shop.save_zone()
    create_shop.page.go_back()
    time.sleep(5)  # todo
    # shops_page.search_shop(shop_name)
    # shops_page.check_search_result(shop_name)
    shops_page.edit_shop()
    create_shop.check_edit_page_opened()
    time.sleep(15)  # долго подгружается картинка todo
    assert compare_image(path_to_image, path_to_reference), 'Zones on plans are different'


@allure.title("Test add sensor to shop")
def test_add_sensor_to_shop(page, create_shop_via_ui, get_config):

    shop_name = create_shop_via_ui
    shops_page = ShopsPage(page)
    shops_page.open(get_config['urls']['host']+'/activate-sensor/d8:3a:dd:c3:60:56')
    activate_sensor_page = ActivateSensorPage(page)
    activate_sensor_page.add_sensor()
    activate_sensor_page.upload_sensor_photo(path.join(path.dirname(__file__), 'test_data', 'sensor_photo.PNG'))
    activate_sensor_page.search_shop(shop_name)
    activate_sensor_page.continue_flow()
    time.sleep(15) # todo долго прогружается схема

    path_to_sensor = path.join(path.dirname(__file__), 'test_data', 'sensor_on_plan.PNG')
    activate_sensor_page.click_on_image(activate_sensor_page.canvas_label,
                                'canvas_screenshot_in_shop_with_zone.png', path_to_sensor)

    activate_sensor_page.setup_position()
    activate_sensor_page.continue_flow('Activate')
    activate_sensor_page.check_success()

    activate_sensor_page.page.go_back()

    sidebar = DashboardPage(page)

    sidebar.open_shops_page()

    shops_page.search_shop(shop_name)
    shops_page.check_search_result(shop_name)
    shops_page.open_shop(shop_name)

    opened_shops = OpenedShopPage(page)
    opened_shops.check_shop_opened()

    path_to_zone = path.join(path.dirname(__file__), 'test_data', 'test_add_sensor_to_shop', 'zone_on_plan.PNG')

    opened_shops.click_on_image(opened_shops.canvas_label,
                                'canvas_screenshot_in_shop_with_zone.png', path_to_zone)

    opened_shops.check_zone_info()


@allure.title("Test open shop")
def test_open_shop(page, create_shop, login):

    shop_name = create_shop
    sidebar = DashboardPage(page)
    sidebar.open_shops_page()
    shops_page = ShopsPage(page)
    shops_page.search_shop(shop_name)
    shops_page.check_search_result(shop_name)

    shops_page.open_shop(shop_name)

    opened_shops = OpenedShopPage(page)
    opened_shops.check_shop_opened()


@allure.title("Test search shop via location")
def test_search_shop_via_location(page, create_shop, login):
    shop_name = create_shop
    sidebar = DashboardPage(page)
    sidebar.open_shops_page()
    shops_page = ShopsPage(page)
    shops_page.search_shop_via_location('Poland')
    shops_page.check_search_result(shop_name, 'Poland')
