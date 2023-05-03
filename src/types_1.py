import httpx


class ExceptionHandler:
    def __call__(self, exp: Exception):
        ...


class ResponseErrorHandler:
    def __call__(
        self,
        response: httpx.Response,
        message: str = None,
        code: str = None,
        errors: dict = None,
    ):
        ...
