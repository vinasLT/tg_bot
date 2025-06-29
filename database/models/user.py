from sqlalchemy import BigInteger, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database.models import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    language = Column(String, default='en', nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    search_history = relationship("UserSearchHistory", back_populates="user")
    find_for_me = relationship("FindForMe", back_populates="user")