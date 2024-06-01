from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    is_active: bool = True
    email: str | None = None
    full_name: str | None = None

    # Tells pydantic this will be used with an orm
    # https://docs.pydantic.dev/1.10/usage/model_config/
    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str
