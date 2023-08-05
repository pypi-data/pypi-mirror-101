from urllib.parse import urljoin

from requests import request

from pythonanywhereapiclient.utils import getenv


class Client:
    def __init__(self, host=None, token=None, user=None):
        self.host = host or getenv('HOST')
        self.token = token or getenv('TOKEN')
        self.user = user or getenv('USER')
        self.base_url = f'https://{self.host}/api/v0/user/{self.user}/'.lower()

    def _construct_endpoint_url(self, endpoint):
        return urljoin(self.base_url, endpoint)

    def _request(self, method, endpoint, data=None, files=None):
        return request(
            method,
            url=self._construct_endpoint_url(endpoint),
            headers=self._headers(),
            data=data,
            files=files,
        )

    def _headers(self):
        return {'Authorization': f'Token {self.token}'}

    def delete(self, endpoint):
        return self._request('DELETE', endpoint)

    def get(self, endpoint):
        return self._request('GET', endpoint)

    def patch(self, endpoint, data=None):
        return self._request('PATCH', endpoint, data=data)

    def post(self, endpoint, data=None, files=None):
        return self._request('POST', endpoint, data=data, files=files)
