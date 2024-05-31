from pydantic import BaseModel


class CollectionBase(BaseModel):
    title: str
    description: str | None = None
    url: str
    imageUrl: str


class CollectionCreate(CollectionBase):
    pass


class Collection(CollectionBase):
    pass

    class Config:
        orm_mode = True
