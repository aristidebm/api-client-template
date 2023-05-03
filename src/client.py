import httpx

from .types_1 import ExceptionHandler, ResponseErrorHandler
from .exceptions import ApiNameException


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
        self._exception_handler = (
            exception_handler or self._get_default_exception_handler()
        )
        self._response_error_handeler = (
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
        method: str,
        endpoint: str,
        *,
        data: dict,
        headers: dict,
        **kwagrs,
    ):
        url = f"{self.base_url}/{endpoint}"

        try:
            response = self.session.build_request(
                url=url,
                method=method,
                data=data,
                headers=headers,
                **kwagrs,
            )
        except Exception as exp:
            self._exception_handler(exp)

        if not response.ok:
            self._response_error_handeler(response)

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
