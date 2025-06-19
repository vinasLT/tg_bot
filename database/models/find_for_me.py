from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.models import Base


class FindForMe(Base):
    __tablename__ = "find_for_me"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String)
    model = Column(String)
    specific_message = Column(String)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="find_for_me")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))