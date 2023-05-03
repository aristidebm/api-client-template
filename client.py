from typing import Callable
import httpx


class Client:
    def __init__(self, base_url: str, session: httpx.Client = None):
        self._base_url = base_url.removesuffix("/")
        self._session = session or self._get_default_session()

    @property
    def base_url(self) -> str:  # immutable
        return self._base_url

    @property
    def session(self) -> httpx.Client:  # immutable
        return self._session

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        data: dict,
        headers: dict,
        exception_handler: Callable = None,
        response_error_handler: Callable = None,
        **kwagrs,
    ):
        url = f"{self.base_url}/{endpoint}"

        exception_handler = exception_handler or self._get_default_exception_handler()

        try:
            response = self.session.build_request(
                url=url, method=method, data=data, headers=headers**kwagrs
            )
        except Exception as exp:
            exception_handler(exp)

        if not response.ok:
            response_error_handler = (
                response_error_handler or self._get_default_reponse_error_handler()
            )
            response_error_handler(response)

        return response.json()

    def _get_default_session(self):
        return httpx.Client()

    def _get_default_exception_handler(self):
        def exception_handler(exp: Exception):
            raise exp
        return exception_handler

    def _get_default_reponse_error_handler(self):
        def response_error_handler(
            response: httpx.Response,
            message: str = None,
            code: str = None,
            errors: dict = None,
        ):
            code = code or response.status_code
            message = message
            errors = errors or {}

            codes_to_exception: dict[str, Exception] = {}

            exception = codes_to_exception.get(code)

            if exception:
                raise exception(
                    message=message,
                    code=code,
                    response=response,
                    errors=errors,
                )

        return response_error_handler
