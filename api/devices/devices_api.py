import allure

from api.base_api import BaseAPI


class DevicesApi(BaseAPI):

    @allure.step('Create device via api request')
    def add_device(self, mac_address=''):

        mac_address = 'd8:3a:dd:c3:55:3b'
        response = self.post(url=self.url+f'/activate-sensor/{mac_address}/')
        return response.json()['data']['createShop']['id']
