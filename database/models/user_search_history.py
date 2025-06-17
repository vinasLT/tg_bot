from datetime import datetime, UTC

from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.models import Base


class UserSearchHistory(Base):
    __tablename__ = "user_search_history"

    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(BigInteger)
    auction_name = Column(String)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="search_history")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))