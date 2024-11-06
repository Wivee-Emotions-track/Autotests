import allure
import requests



@allure.id("5")
def test_delete_device_wby_id():


    with allure.step("Delete device"):

        device_id = 262
        url = "https://app-staging.wayvee.com/graphql"

        mutation = """
        mutation DeleteProducedDevice($id: ID!) {
          deleteProducedDevice(id: $id) {
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
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(
            url,
            json={
                "query": mutation,
                "variables": variables
            }
        )
        data = response.json()


