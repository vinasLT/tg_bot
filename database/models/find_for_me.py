from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.models import Base


class FindForMe(Base):
    __tablename__ = "find_for_me"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String)
    model = Column(String)
    year_from = Column(Integer)
    year_to = Column(Integer)
    budget_from = Column(String)
    budget_to = Column(String)
    specific_message = Column(String, nullable=True, default=None)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="find_for_me")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))