import allure

from api.base_api import BaseAPI


class TokenApi(BaseAPI):

    @allure.step('Create token api request')
    def create_token(self, token_name):

        query = """
        mutation CreateToken($name: String!) {
            createApiToken(name: $name) {
                id
                name
                userInfo {
                    id
                    email
                    __typename
                }
                createdAt
                revokedAt
                signedJWT
                __typename
            }
        }
        """

        variables = {
            "name": token_name
        }

        payload = {
            "operationName": "CreateToken",
            "query": query,
            "variables": variables
        }

        response = self.post(url=self.url, json=payload)
        return response.json()['data']['createApiToken']['id']

    @allure.step("revoke token via api")
    def revoke_token(self, token_id, check_response=True):

        query = """
            mutation RevokeToken($id: ID!) {
                revokeApiToken(id: $id) {
                    id
                    name
                    userInfo {
                        id
                        email
                        __typename
                    }
                    createdAt
                    revokedAt
                    signedJWT
                    __typename
                }
            }
            """
        variables = {
            "id": token_id
        }

        payload = {
            "operationName": "RevokeToken",
            "query": query,
            "variables": variables
        }
        if not check_response:
            try:
                self.post(url=self.url, json=payload)
            except self.APIException:
                pass

    def get_token_list(self, user_id="128"):
        query = """
            query tokensList($userId: ID) {
                apiTokens(userId: $userId) {
                    nodes {
                        id
                        name
                        userInfo {
                            id
                            email
                            __typename
                        }
                        createdAt
                        revokedAt
                        signedJWT
                        __typename
                    }
                    page {
                        page
                        perPage
                        __typename
                    }
                    __typename
                }
            }
            """

        variables = {
            "userId": user_id
        }

        payload = {
            "operationName": "tokensList",
            "query": query,
            "variables": variables
        }

        response = self.post(url=self.url, json=payload)
        return response.json()['data']['apiTokens']['nodes']
