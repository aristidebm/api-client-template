from .client import ApiClient


class Service:
    def __init__(self, client: ApiClient):
        self._client = client

    @property
    def client(self) -> ApiClient:
        return self._client

    def command(self, *args, **kwargs):
        endpoint = "/command"
        method = "POST"
        data = {}
        headers = {}
        self.client.request(
            method=method, endpoint=endpoint, data=data, headers=headers
        )

    def query(self, *args, **kwargs):
        endpoint = "/query"
        method = "GET"
        params = {}
        headers = {}
        return self.client.request(
            method=method, endpoint=endpoint, params=params, headers=headers
        )
