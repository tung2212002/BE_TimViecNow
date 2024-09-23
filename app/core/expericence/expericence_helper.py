from sqlalchemy.orm import Session

from app import crud
from app.common.exception import CustomException
from fastapi import status


class ExperienceHelper:
    def check_valid(
        self,
        db: Session,
        id: int,
    ) -> int:
        experience = crud.experience.get(db, id)
        if not experience:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Experience not found"
            )
        return id


experience_helper = ExperienceHelper()
