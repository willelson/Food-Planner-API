from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime)
    last_updated = Column(DateTime)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="recipe")

    recipes = relationship("Collection", back_populates="recipes")
