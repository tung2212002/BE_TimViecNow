from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import JobPosition
from app.schema.job_position import (
    JobPositionCreate,
    JobPositionUpdate,
)


class CRUDJobPosition(CRUDBase[JobPosition, JobPositionCreate, JobPositionUpdate]):
    pass


job_position = CRUDJobPosition(JobPosition)
