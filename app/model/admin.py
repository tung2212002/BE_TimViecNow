from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.hepler.enum import Gender
from app.db.base_class import Base


class Admin(Base):
    id = Column(
        Integer,
        ForeignKey("manager.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    is_verified = Column(Boolean, default=False)
    gender = Column(Enum(Gender), nullable=True)

    manager = relationship(
        "Manager",
        back_populates="admin",
        uselist=False,
        single_parent=True,
        passive_deletes=True,
    )
    approval_log = relationship("ApprovalLog", back_populates="admin")
