from datetime import datetime
from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    description: str | None = None
    source_url: str
    imageUrl: str
    created_at: datetime
    last_updated: datetime


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    pass

    class Config:
        from_attributes = True
