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

    def search_shop_via_name(self, shop_name):

        query = """
        query ListShops($userId: ID, $name: String, $pageInput: PageInput) {
            shops(pageInput: $pageInput, name: $name, userId: $userId) {
                nodes {
                    id
                    name
                    location
                    industry
                    traffic
                    openHours
                    openHoursWeekend
                    timeZone
                    createdAt
                    status
                    planUrl
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
            "name": shop_name,
            "pageInput": {
                "page": 1,
                "perPage": 10
            }
        }

        response = self.post(url=self.url, json={"query": query, "variables": variables})
        return response.json()['data']['shops']['nodes'][0]

    @allure.step('Remove shop via id')
    def delete_shop(self, shop_id):

        query = """
            mutation DeleteShop($id: ID!) {
                deleteShop(id: $id) {
                    id
                    name
                }
            }
        """

        variables = {
            "id": shop_id
        }

        response = self.post(url=self.url, json={"query": query, "variables": variables})
        return response.json()
