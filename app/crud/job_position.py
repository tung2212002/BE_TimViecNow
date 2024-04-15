from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import JobPosition, GroupPosition
from app.schema.job_position import (
    JobPositionItemResponse,
    JobPositionCreateRequest,
    JobPositionUpdateRequest,
)


class CRUDCategory(
    CRUDBase[JobPosition, JobPositionCreateRequest, JobPositionUpdateRequest]
):
    pass


job_position = CRUDCategory(JobPosition)
