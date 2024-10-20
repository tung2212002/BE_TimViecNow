from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Manager(Base):
    id = Column(
        Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(10), nullable=False)

    admin = relationship(
        "Admin",
        back_populates="manager",
        lazy=True,
        uselist=False,
        passive_deletes=True,
    )
    business = relationship(
        "Business",
        back_populates="manager",
        lazy=True,
        uselist=False,
        passive_deletes=True,
    )
    account = relationship("Account", back_populates="manager", uselist=False)
