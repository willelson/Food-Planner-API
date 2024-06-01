from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    # Tells pydantic this will be used with an orm
    # https://docs.pydantic.dev/1.10/usage/model_config/
    class Config:
        from_attributes = True
