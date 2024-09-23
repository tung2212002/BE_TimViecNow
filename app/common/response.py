from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class CustomResponse(JSONResponse):
    def __init__(
        self,
        *,
        status_code: int = 200,
        msg: str = None,
        status: str = "success",
        data: dict = None
    ):
        content = jsonable_encoder(
            {
                "status": status,
                "message": msg,
                "data": {} if isinstance(data, str) else data,
            }
        )
        super().__init__(status_code=status_code, content=content)
