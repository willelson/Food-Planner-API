from datetime import datetime
from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    description: str | None = None
    source_url: str
    image_url: str
    created_at: datetime
    last_updated: datetime


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int

    class Config:
        from_attributes = True
