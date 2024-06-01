from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class CalendarEntry(Base):
    __tablename__ = "calendar_entries"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    entry_date = Column(DateTime, index=True)

    recipe_id = relationship("Recipe", back_populates="recipes")

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="calendar_entries")
