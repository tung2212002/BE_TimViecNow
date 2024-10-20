from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException

from app.common.exception import CustomException


async def validation_error_handler(
    request: Request, exc: RequestValidationError | ValidationError
) -> JSONResponse:
    error = exc.errors()[0]
    if error["type"] == "json_invalid":
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid JSON body"},
        )
    error_input = error["loc"][0]
    error_msg = error["msg"]
    field = error["loc"][-1]
    message = f"{field} : {error_msg}"

    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": message},
    )


def register_exception(app: FastAPI):
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.msg,
                **({"data": exc.data} if exc.data else {}),
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError | ValidationError
    ):
        return await validation_error_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError | ValidationError
    ):
        return await validation_error_handler(request, exc)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.detail,
            },
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        if isinstance(exc, CustomException):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "status": "error",
                    "message": exc.msg,
                    **({"data": exc.data} if exc.data else {}),
                },
                background=exc.background_tasks,
            )
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error.",
            },
        )
