import allure

from api.base_api import BaseAPI


class UsersApi(BaseAPI):

    @allure.step('Create user via api request')
    def create_user(self, email, password, send_email=False):
        query = """
        mutation CreateUser($email: String!, $password: String!, $sendEmail: Boolean) {
          createUser(email: $email, password: $password, sendEmail: $sendEmail) {
            id
            email
            isAdmin
            canViewCSATOnly
            canDoCSATOnly
            verifiedAt
          }
        }
        """

        variables = {
            "email": email,
            "password": password,
            "sendEmail": send_email
        }

        # payload = {
        #     "query": query,
        #     "variables": variables
        # }

        response = self.post(url=self.url, json={"query": query, "variables": variables})
        return response.json()['data']['createShop']['id']

    @allure.step('Delete user via api request')
    def delete_user(self, user_id):

        query = """
        mutation DeleteUser($id: ID!) {
          deleteUser(id: $id)
        }
        """

        variables = {
            "id": user_id  # Замените на ID пользователя, которого хотите удалить
        }

        self.post(url=self.url, json={"query": query, "variables": variables})
