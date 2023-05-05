# api-client-template

A template to  consume rest-api in python code

## Package structure

```
.
├── client.py       contains a client that exposes a generic request method and accepts `session` as instantiation parameter and api base-url and so on.
├── .env.example    contains envrionment variable declarations.
├── environment.py  contains environment variables load as language (Python|JS) objects
├── exceptions.py   contains custom exceptions related to the target api.
├── __init__.py     exports the client, the services and the exceptions.
├── README.md
├── services.py     contains queries and commands related to the target api.
└── session.py      contains transport layer configuration struff (max-retries, rate-limits, exponential-backoff, ..)
└── types.py        contains request and response declarations.

```

## Depencencies graph

```
- session --use--> environment
- client --use--> session
- client --[use]--> exceptions
- services --use--> client, exceptions, types, environment
```

## Guidelines

+ Always define custom exceptions for the target Api.

+ Always define a base exception for the target Api.

+ Always seperate exceptions into two groups `techinal` and `business` that will inherit from the base exception.

+ Always translate `technical` exceptions into `business` exceptions (when the client is business oriented, in this case use are less technical person, so they don't need to know about technical information)

+ Always translate `transport` layer exceptions into `technical`, but when doing so make sure not to loose the exception context, you have to chain the translated exception and it's cause.

+ Always throw an exception when the `query` or the `command` cannot be fullill, avoid returning error codes or boolean, you can't the task in your hand you just fail and fail fast.

+ Never handle an exception (you can translate but don't catch and log, cause you don't know how the user of library will want to handle exception).

+ Always write the happy part of the code, if you cannot do something, just throw an exception, avoid guessing.

+ Try not do validate input parameters inside the `query` or a `command` itself, define a wrapper that will do it before passing parameters to the wrappee.

+ Always translate(map) Http error-code to exception. 

+ All Custom exception must have the shape below:

```python
from __future__ import annotations
# definition

class APIException(Exception):
    def __init__(
        self,
        message: str = None,
        code: str = None,
        errors: dict = None,
        response: Response = None
    ):
        self.message = message
        self.code = code
        self.errors = errors or {}
        self.response = response
    
    @property
    def cause(self) -> Exception | None:
        return self.__cause__

# Usage
raise APIException(
    message="message",
    code="validation_error",
    errors={},
    response=response,
) from causeExceptionInstance # Chain the cause

```
+ The client must throw only throw technical errors.
+ The service must throw only throw business errors.

## Exception handling flow
![Exception handling flow diagram](docs/Exception-handling-flow-in-api-clients.png)

## Case studies  
