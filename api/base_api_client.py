from urllib.parse import urljoin
import requests


class BaseApiClient:

    def __init__(self,
                 endpoint: str = "http://localhost/",
                 token: str = None,
                 auth_prefix: str = 'Bearer'):
        self.auth_prefix = auth_prefix
        self.token = token
        self.endpoint = endpoint.rstrip('/') + '/'
        self.verify = False
        self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def _set_headers(self, use_token, content_type, headers):
        headers['Content-Type'] = content_type
        if use_token:
            headers['Authorization'] = f'{self.auth_prefix} {self.token}'
        return headers

    def _handle_error(self, response):
        try:
            server_msg = response.json()
        except ValueError:
            server_msg = response.text or response.reason

        raise BadApiStatusCode(
            f"Status Code: {response.status_code}; Message From Server: {server_msg}",
            status_code=response.status_code,
            server_message=server_msg
        )

    def _convert_response_to_json(self, response):
        """Converts the response to JSON and optionally reduces nested structures."""
        try:
            result = response.json()
        except ValueError:
            return response.text

        if result:
            while len(result) == 1 and not isinstance(result, list):
                if isinstance(result, dict):
                    data = next(iter(result.values()))
                else:
                    data = next(iter(result))
                if isinstance(data, (dict, list)):
                    result = data
                else:
                    break
        return result

    def basic_request(self, method, url_path: str,
                      endpoint: str = None,
                      use_token: bool = False,
                      content_type: str = 'application/json',
                      check_response=True,
                      ok_codes: set = {200, 201, 204},
                      convert_to_json: bool = True,
                      **kwargs) -> requests.Response:

        kwargs['headers'] = self._set_headers(use_token, content_type, kwargs.get('headers', {}))

        response = self.session.request(
            method,
            url=urljoin(endpoint or self.endpoint, url_path),
            verify=self.verify,
            **kwargs
        )

        if check_response and response.status_code not in ok_codes:
            self._handle_error(response)

        if convert_to_json:
            return self._convert_response_to_json(response)

        return response

    # HTTP methods
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


class BadApiStatusCode(Exception):
    def __init__(self, message, status_code=None, server_message=None):
        super().__init__(message)
        self.status_code = status_code
        self.server_message = server_message
