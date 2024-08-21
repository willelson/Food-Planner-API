from datetime import datetime

from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    description: str | None = None
    source_url: str
    image_url: str
    ingredients: str | None = None
    method: str | None = None
    servings: int | None = None
    cooking_time: str | None = None


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class Recipe(RecipeBase):
    created_at: datetime
    last_updated: datetime
    id: int

    class Config:
        from_attributes = True
