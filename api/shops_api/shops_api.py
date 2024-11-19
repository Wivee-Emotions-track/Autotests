import allure

from api.base_api import BaseAPI


class ShopsApi(BaseAPI):

    @allure.step('Create shop via api request')
    def create_shop(self, plan_path, **shop_info):

        # metadata = {
        #     "name": shop_info['shop_name'],
        #     "location": shop_info['location'],
        #     "timeZone": shop_info['timezone'],
        #     "industry": shop_info['timezone'],
        #     "traffic": shop_info['traffic'],
        #     "openHours": "11:30 - 15:45",
        #     "openHoursWeekend": ""
        # }

        variables = {
            "metadata": {
                "name": shop_info['shop_name'],
                "location": shop_info['location'],
                "timeZone": shop_info['timezone'],
                "industry": shop_info['industry'],
                "traffic": shop_info['traffic'],
                "openHours": "11:30 - 15:45",
                "openHoursWeekend": ""
            },
            "zones": []
        }
        query = """
        mutation createShop($metadata: ShopMetaDataInput!, $zones: [ZoneInstanceInput!]!) {
          createShop(shopMetaDataInput: $metadata, zones: $zones) {
            id
            name
            location
            timeZone
            industry
            traffic
            openHours
            openHoursWeekend
          }
        }
        """

        # graphql_query = {
        #     "operationName": "createShop",
        #     "variables": {
        #         "file": None,
        #         "zones": [],
        #         "metadata": metadata
        #     },
        #     "query": """
        #         mutation createShop($file: Upload, $metadata: ShopMetaDataInput!,
        #          $vertices: ArrayVerticesInput, $zones: [ZoneInstanceInput!]!) {
        #           createShop(
        #             plan: $file
        #             shopMetaDataInput: $metadata
        #             vertices: $vertices
        #             zones: $zones
        #           ) {
        #             id
        #             name
        #             location
        #             industry
        #             traffic
        #             openHours
        #             openHoursWeekend
        #             timeZone
        #             __typename
        #           }
        #         }
        #         """
        # }

        # multipart_data = {
        #     "operations": (None, str(graphql_query)),
        #     "map": (None, '{"1":["variables.file"]}'),
        #     "1": (plan_path.split("/")[-1], open(plan_path, "rb"), "image/png")
        # }

        # response = self.post(url=self.url, files=multipart_data)
        response = self.post(url=self.url, json={"query": query, "variables": variables})
        return response.json()['data']['createShop']['id']
