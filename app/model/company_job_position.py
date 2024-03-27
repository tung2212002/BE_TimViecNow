from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CompanyJobPosition(Base):
    company_id = Column(
        Integer, ForeignKey("company.id", ondelete="CASCADE"), index=True
    )
    job_position_id = Column(
        Integer, ForeignKey("job_position.id", ondelete="CASCADE"), index=True
    )
