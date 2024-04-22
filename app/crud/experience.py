from sqlalchemy.orm import Session

from app.model.job_experience import JobExperience


class CRUDExperience:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int) -> JobExperience:
        return db.query(self.model).filter(self.model.id == id).first()


experience = CRUDExperience(JobExperience)
