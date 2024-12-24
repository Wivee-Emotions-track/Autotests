import requests


class IndustrialApi:
    def __init__(self, url):

        self.url = url

    def add_device(self, token, device_version="v1", device_mode="Camera", date='2023-01-01', mac='',
                   check_response=True):

        payload = {
            "deviceVersion": device_version,
            "deviceModification": device_mode,
            "manufacturingDate": date,
            "macAddress": mac
        }
        headers = {
          'Accept': 'application/json',
          'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", self.url+'/industrial/registerDevice', headers=headers, json=payload)
        if check_response:
            self.check_response(response)
        return response

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
