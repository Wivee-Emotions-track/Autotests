import time
from datetime import datetime
from os import path

import allure
from ui.pages.create_shop_page import CreateShopPage
from ui.pages.shops_page import ShopsPage


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
