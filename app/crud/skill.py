from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import Skill
from app.schema.skill import SkillItemResponse, SkillCreate, SkillUpdate


class CRUDSkill(CRUDBase[Skill, SkillCreate, SkillUpdate]):
    def get_by_name(self, db: Session, name: str) -> Skill:
        return db.query(self.model).filter(self.model.name == name).first()


skill = CRUDSkill(Skill)
