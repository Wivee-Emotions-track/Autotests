import logging
import time
import json
import requests


class BaseAPI:
    """ Base class for any API class. Contains basic methods for API requests."""

    __EXCEPTION_LIST = []

    def __init__(self):
        # self.config = get_env_configs(env)
        # self.config = config
        self.logger = logging.getLogger("TestLogger")

        self.url = "https://app-staging.wayvee.com/graphql"
        self.login = 'dmitrijdmtirij@gmail.com'
        self.password = 'Qwerty_0000'
        self.session = requests.Session()
        self.session.headers = \
            {'Content-Type': 'application/json',
             'Cookie': f"auth-token={self.get_token(self.login, self.password)}"}

    def __del__(self):
        self.session.close()

    def basic_request(self, method, endpoint=None, url=None, steps=1, delay=3, **kwargs) -> requests.Response:
        response = requests.Response()
        step = 0
        while step < steps:
            response = self.session.request(method, url=url or (self.url + endpoint), **kwargs)

            try:
                self.check_response(response)
                return response

            except BaseAPI.APIException as error:
                if any(exception in error.message for exception in self.__EXCEPTION_LIST):
                    steps = 6
                    delay = 10
                logging.getLogger('TestLogger').warning('Request %s/%s failed. '
                                                        'Retry in %s seconds', step + 1, steps, delay)
                time.sleep(delay)
                step += 1
        logging.getLogger("TestLogger").error('API request failed after %s retries', steps)
        return self.check_response(response)

    def post(self, **kwargs):
        return self.basic_request(method='post', **kwargs)

    def get(self, **kwargs):
        return self.basic_request(method='get', **kwargs)

    def put(self, **kwargs):
        return self.basic_request(method='put', **kwargs)

    def patch(self, **kwargs):
        return self.basic_request(method='patch', **kwargs)

    def delete(self, **kwargs):
        return self.basic_request(method='delete', **kwargs)

    class APIException(Exception):
        """ Class for any API exceptions during requests."""

        def __init__(self, message=''):
            self.message = message
            logging.getLogger("TestLogger").debug(self.message)

        def __str__(self):
            return self.message

    def check_response(self, response):

        response_info = f'URL: {response.url}\n' \
                        f'Response time: {response.elapsed}\n' \
                        f'Response status: {response.status_code}\n'

        if not response.ok:
            response_info += f'Response body: {response.text}\n'
            raise self.APIException(response_info)

        json_response = response.json()
        if "errors" in json_response and json_response["errors"]:
            response_info += f'GraphQL Errors: {json_response["errors"]}\n'
            raise self.APIException(f"GraphQL errors occurred:\n{response_info}")

        logging.getLogger("TestLogger").debug('\nRequest_info:\n%s', response_info)

        return response

    def get_token(self, login, password):

        auth_query = """
                mutation SignIn($email: String!, $password: String!) {
                    signIn(email: $email, password: $password) {
                        id
                        __typename
                    }
                }
            """

        auth_response = requests.post(
            self.url,
            json={'query': auth_query, 'variables': {'email': login, 'password': password}}
        )
        self.check_response(auth_response)
        auth_cookie = auth_response.headers.get("Set-Cookie")
        token = auth_cookie.split("auth-token=")[1].split(";")[0]
        return token
