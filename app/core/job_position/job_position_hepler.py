from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.schema import (
    job_position as job_position_schema,
    group_position as group_position_schema,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.model import JobPosition, GroupPosition
from app.core.helper_base import HelperBase


class JobPositionHelper(HelperBase):
    def validate_position_group_create(self, data: dict):
        try:
            return group_position_schema.GroupPositionCreateRequest(**data)
        except Exception as e:
            return custom_response_error(
                status_code=400,
                status=constant.ERROR,
                response=get_message_validation_error(e),
            )

    def validate_position_group_update(self, data: dict):
        try:
            return group_position_schema.GroupPositionUpdateRequest(**data)
        except Exception as e:
            return custom_response_error(
                status_code=400,
                status=constant.ERROR,
                response=get_message_validation_error(e),
            )

    def check_valid(
        self,
        db: Session,
        id: int,
    ) -> int:
        position = crud.job_position.get(db, id)
        if not position:
            return custom_response_error(
                status_code=404, status=constant.ERROR, response="Position not found"
            )
        return id

    def get_info(self, db: Session, position: JobPosition):
        return job_position_schema.JobPositionItemResponse(**position.__dict__)

    def get_list_info(self, db: Session, positions: List[JobPosition]):
        return [self.get_info(db, position) for position in positions]

    def get_group_info(self, db: Session, group: GroupPosition):
        return group_position_schema.GroupPositionItemResponse(**group.__dict__)

    def get_list_group_info(self, db: Session, groups: List[GroupPosition]):
        return [self.get_group_info(db, group) for group in groups]


job_position_helper = JobPositionHelper(
    schema_page.Pagination,
    job_position_schema.JobPositionCreateRequest,
    job_position_schema.JobPositionUpdateRequest,
)
