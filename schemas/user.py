from pydantic import BaseModel
from schemas.collection import Collection
from schemas.recipe import Recipe


class UserBase(BaseModel):
    username: str
    email: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    full_name: str | None = None
    recipes: list[Recipe] = []
    collections: list[Collection] = []

    # Tells pydantic this will be used with an orm
    # https://docs.pydantic.dev/1.10/usage/model_config/
    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str
