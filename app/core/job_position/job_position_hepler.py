from sqlalchemy.orm import Session
from typing import List

from app.crud import job_position as job_positionCRUD
from app.schema.job_position import JobPositionItemResponse
from app.schema.group_position import GroupPositionItemResponse
from app.model import JobPosition, GroupPosition
from fastapi import status
from app.common.exception import CustomException


class JobPositionHelper:
    def check_valid(
        self,
        db: Session,
        id: int,
    ) -> int:
        position = job_positionCRUD.get(db, id)
        if not position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Position not found"
            )
        return id

    def get_info(self, db: Session, position: JobPosition):
        return JobPositionItemResponse(**position.__dict__)

    def get_list_info(self, db: Session, positions: List[JobPosition]):
        return [self.get_info(db, position) for position in positions]

    def get_group_info(self, db: Session, group: GroupPosition):
        return GroupPositionItemResponse(**group.__dict__)

    def get_list_group_info(self, db: Session, groups: List[GroupPosition]):
        return [self.get_group_info(db, group) for group in groups]


job_position_helper = JobPositionHelper()
