from sqlalchemy.orm import Session

from app.crud import experience as experienceCRUD
from app.common.exception import CustomException
from fastapi import status


class ExperienceHelper:
    def check_valid(
        self,
        db: Session,
        id: int,
    ) -> int:
        experience = experienceCRUD.get(db, id)
        if not experience:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Experience not found"
            )
        return id


experience_helper = ExperienceHelper()
