from sqlalchemy.orm import Session

from app.core import constant
from app.hepler.response_custom import custom_response_error
from app import crud


class ExperienceHelper:
    def check_valid(
        self,
        db: Session,
        id: int,
    ) -> int:
        experience = crud.experience.get(db, id)
        if not experience:
            return custom_response_error(
                status_code=404, status=constant.ERROR, response="Experience not found"
            )
        return id


experience_helper = ExperienceHelper()
