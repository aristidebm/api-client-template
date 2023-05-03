import httpx


class ApiNameException(Exception):
    def __init__(
        self,
        message: str = None,
        code: str = None,
        errors: dict = None,
        response: httpx.Response = None,
    ):
        self.message = message
        self.code = code
        self.errors = errors or {}
        self.response = response

    @property
    def cause(self) -> Exception | None:
        return self.__cause__


class ApiNameBusinessException(ApiNameException):
    ...


class ApiNameTechinalException(ApiNameException):
    ...


class ApiNameCommandExecutionException(ApiNameBusinessException):
    ...


class ApiNameQueryExectutionException(ApiNameBusinessException):
    ...
