from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.hepler.enum import Gender
from app.db.base_class import Base


class Admin(Base):
    # manager_base_id = Column(
    #     Integer,
    #     ForeignKey("manager_base.id", ondelete="CASCADE"),
    #     primary_key=True,
    #     index=True,
    # )
    id = Column(
        Integer,
        ForeignKey("manager_base.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    is_verified = Column(Boolean, default=False)
    phone_number = Column(String(10), nullable=False)
    gender = Column(Enum(Gender), nullable=True)

    manager_base = relationship(
        "ManagerBase",
        back_populates="admin",
        uselist=False,
        single_parent=True,
        passive_deletes=True,
    )
    approval_log = relationship("ApprovalLog", back_populates="admin")
