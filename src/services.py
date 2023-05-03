from .client import Client


class Service:
    def __init__(self, client: Client):
        self._client = client

    @property
    def client(self) -> Client:  # immutable
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
        data = {}
        headers = {}
        return self.client.request(
            method=method, endpoint=endpoint, data=data, headers=headers
        )
