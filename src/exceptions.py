import httpx

class APINameException(Exception):
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


class ApiNameBusinessException(APINameException):
    ...


class ApiNameTechinalException(APINameException):
    ...


class ApiNameCommandExecutionException(ApiNameBusinessException):
    ...


class ApiNameQueryExectutionException(ApiNameBusinessException):
    ...
