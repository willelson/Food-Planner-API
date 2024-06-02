from datetime import datetime

from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    description: str | None = None
    source_url: str
    image_url: str


class RecipeCreate(RecipeBase):
    created_at: datetime


class RecipeUpdate(RecipeBase):
    pass


class Recipe(RecipeBase):
    created_at: datetime
    last_updated: datetime
    id: int

    class Config:
        from_attributes = True
