from datetime import datetime
from pydantic import BaseModel


class CollectionBase(BaseModel):
    title: str
    description: str | None = None
    created_at: datetime
    last_updated: datetime


class CollectionCreate(CollectionBase):
    pass


class Collection(CollectionBase):
    pass

    class Config:
        orm_mode = True
