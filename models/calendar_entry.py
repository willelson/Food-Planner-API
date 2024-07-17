from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from database import Base


class CalendarEntry(Base):
    __tablename__ = "calendar_entries"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    entry_date = Column(DateTime, index=True)

    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipe")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

    def __repr__(self):
        return (
            f"Calendar entry - user: {self.user.username} | recipe: {self.recipe.title}"
        )
