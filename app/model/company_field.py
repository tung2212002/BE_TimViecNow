from sqlalchemy import Column, ForeignKey, Integer, event
from sqlalchemy.orm import relationship, Session

from app.db.base_class import Base
from app.model.field import Field


class CompanyField(Base):
    company_id = Column(
        Integer, ForeignKey("company.id", ondelete="CASCADE"), index=True
    )
    field_id = Column(Integer, ForeignKey("field.id", ondelete="CASCADE"), index=True)

    company = relationship(
        "Company",
        back_populates="company_field_secondary",
        overlaps="fields",
    )
    field = relationship(
        "Field",
        back_populates="company_field_secondary",
        overlaps="fields",
    )


@event.listens_for(CompanyField, "after_insert")
def receive_after_insert(mapper, connection, target):
    session = Session(bind=connection)
    field = session.query(Field).filter(Field.id == target.field_id).first()
    field.count += 1
    session.commit()
    session.close()


@event.listens_for(CompanyField, "after_delete")
def receive_after_delete(mapper, connection, target):
    session = Session(bind=connection)
    field = session.query(Field).filter(Field.id == target.field_id).first()
    field.count -= 1
    session.commit()
    session.close()
