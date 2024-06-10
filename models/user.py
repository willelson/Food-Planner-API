from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    collections = relationship("Collection", back_populates="user")
    recipes = relationship("Recipe", back_populates="user")
    calendar_entries = relationship("CalendarEntry", back_populates="user")

    def __repr__(self):
        return f"User: {self.username}"
