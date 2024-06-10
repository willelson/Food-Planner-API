from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base

collection_recipes = Table(
    "collection_recipes",
    Base.metadata,
    Column("collection_id", ForeignKey("collections.id"), primary_key=True),
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
)


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime)
    last_updated = Column(DateTime, default=datetime.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="collections")

    recipes = relationship(
        "Recipe", secondary=collection_recipes, back_populates="collections"
    )

    def __repr__(self):
        return f"Collection: {self.title}"


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    source_url = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime)
    last_updated = Column(DateTime, default=datetime.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="recipes")

    collections = relationship(
        "Collection", secondary=collection_recipes, back_populates="recipes"
    )

    calendar_entries = relationship(
        "CalendarEntry", back_populates="recipe", cascade="delete"
    )

    def __repr__(self):
        return f"Recipe {self.title}"
