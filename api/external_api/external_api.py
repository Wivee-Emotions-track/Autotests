import requests

url = "https://api.app-staging.wayvee.com/"


class ExternalApi:

    def get_shops_list(self, token, check_response=True):

        payload = {}
        headers = {
          'Accept': 'application/json',
          'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url + "/v1/shops", headers=headers, data=payload)
        if check_response:
            self.check_response(response)

    def check_response(self, response):
        response_info = f'URL: {response.url}\n' \
                        f'Response time: {response.elapsed}\n' \
                        f'Response status: {response.status_code}\n'

        if not response.ok:
            response_info += f'Response body: {response.content}\n'
            response_info += f'Request body: {response.request.body}'
            raise self.APIException(response_info)

        return response

    class APIException(Exception):
        """ Class for any API exceptions during requests."""

        def __init__(self, message=''):
            self.message = message

        def __str__(self):
            return self.message
