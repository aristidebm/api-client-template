import httpx

from .exceptions import ApiNameException
from .types_1 import ExceptionHandler, ResponseErrorHandler


class ApiClient:
    def __init__(
        self,
        base_url: str,
        session: httpx.Client = None,
        *,
        exception_handler: ExceptionHandler = None,
        response_error_handler: ResponseErrorHandler = None,
    ):
        self._base_url = base_url.removesuffix("/")
        self._session = session or self._get_default_session()
        self.session.base_url = base_url
        self._exception_handler = (
            exception_handler or self._get_default_exception_handler()
        )
        self._response_error_handler = (
            response_error_handler or self._get_default_reponse_error_handler()
        )

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def session(self) -> httpx.Client:
        return self._session

    def request(
        self,
        endpoint: str,
        *,
        method: str = None,
        data: dict = None,
        headers: dict = None,
        params: str = None,
        **kwagrs,
    ):
        try:
            response = self.session.request(
                url=endpoint,
                method=method,
                data=data,
                headers=headers,
                params=params**kwagrs,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exp:
            self._response_error_handler(exp.response)
            # self.session.close()
        except Exception as exp:
            self._exception_handler(exp)
            # self.session.close()

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
            code = code
            message = message
            errors = errors or {}

            codes_to_exception: dict[str, ApiNameException] = {}

            exception = codes_to_exception.get(code)

            if exception:
                raise exception(
                    message=message,
                    code=code,
                    response=response,
                    errors=errors,
                )

        return response_error_handler
