from sqlalchemy.orm import Session

from app.crud import (
    job_approval_log as job_approval_logCRUD,
)
from app.schema import (
    job_approval_log as schema_job_approval_log,
)


def create_job_approval_log(
    db: Session, data: schema_job_approval_log.JobApprovalLogCreate
):
    job_approval_log = job_approval_logCRUD.create(db, obj_in=data)
    return job_approval_log
