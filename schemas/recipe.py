from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    description: str | None = None
    url: str
    imageUrl: str


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    pass

    class Config:
        orm_mode = True
