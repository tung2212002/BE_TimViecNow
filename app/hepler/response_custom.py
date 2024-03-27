from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.core import constant


def custom_response(
    status_code: int, status: str, response: dict = None
) -> JSONResponse:
    """
    Custom response.

    This function allows creating a custom response.

    Parameters:
    - status_code (int): The status code of the response.
    - status (str): The status of the response.
    - data (dict): The data of the response.

    Returns:
    - response (JSONResponse): The response.
    """
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            {
                "status": status,
                "message": response if isinstance(response, str) else "",
                "data": response if isinstance(response, dict) else {},
            }
        ),
    )


def custom_response_error(status_code: int, status: str, response: any) -> JSONResponse:
    """
    Custom response error.

    This function allows creating a custom response error.

    Parameters:
    - status_code (int): The status code of the response.
    - status (str): The status of the response.
    - response (any): The response.

    Returns:
    - response (JSONResponse): The response.
    """
    return JSONResponse(
        status_code=status_code,
        content={"status": status, "message": response if response else "Error"},
    )
