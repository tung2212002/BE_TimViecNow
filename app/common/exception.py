from typing import Any
from starlette.background import BackgroundTasks


class CustomException(Exception):
    status_code: int

    def __init__(
        self,
        *,
        status_code: int = 400,
        msg: str = None,
        data: Any = None,
        background_tasks: BackgroundTasks | None = None
    ):
        self.msg = msg
        self.data = data
        self.background_tasks = background_tasks
        self.status_code = status_code
