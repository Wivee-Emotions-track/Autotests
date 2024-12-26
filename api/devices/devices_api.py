import allure

from api.base_api import BaseAPI


class DevicesApi(BaseAPI):

    @allure.step('Activate device via api request')
    def activate_device(self, mac_address=''):

        mac_address = 'd8:3a:dd:c3:55:3b'
        response = self.post(url=self.url+f'/activate-sensor/{mac_address}/')
        return response.json()['data']['createShop']['id']

    @allure.step('Delete user via api request')
    def delete_user(self, user_id):

        query = """
        mutation DeleteUser($id: ID!) {
          deleteUser(id: $id)
        }
        """

        variables = {
            "id": user_id
        }

        self.post(url=self.url, json={"query": query, "variables": variables})

    def delete_device(self, device_id):

        query = """
            mutation DeleteProducedDevice($id: ID!) {
                deleteProducedDevice(id: $id) {
                    id
                    version
                    modification
                    macAddress
                    manufacturingDate
                }
            }
        """

        variables = {
            "id": device_id
        }

        self.post(url=self.url, json={"query": query, "variables": variables})

    def get_devices(self):
        query = """
            query ProducedDevices($pageInput: PageInput) {
                producedDevices(pageInput: $pageInput) {
                    nodes {
                        id
                        version
                        greenGrassId
                        modification
                        macAddress
                        manufacturingDate
                    }
                    page {
                        page
                        perPage
                        totalItems
                    }
                }
            }
        """
        variables = {
            "pageInput": {
                "page": 5,
                "perPage": 10
            }
        }

        response = self.post(url=self.url, json={"query": query, "variables": variables})
        return response.json()['data']['producedDevices']['nodes']
