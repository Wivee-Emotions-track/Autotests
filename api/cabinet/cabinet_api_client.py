import json

from api.base_api_client import BaseApiClient



class CabinetApiClient(BaseApiClient):
    """The api client for https://cabinet.snmt.dev/swagger/"""


    def __init__(self,
                 endpoint,
                 user_id=None,
                 password=None):
        self.user_id = user_id
        self.password = password
        super().__init__(f'{endpoint}/')



    def post_access_api_token_from_auth_token(self):
        """Get access token for services api"""
        data = json.dumps({
            "scope": [
                "report_builder", "meet_extension"
            ],
            "user_id": self.user_id,
            "auth_token": self.password
        })

        return self.post(url_path=f'api/users/api-access/access-api-token-from-auth-token/', data=data)
