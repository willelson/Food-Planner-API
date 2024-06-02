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
    id: int

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "id": 33,
                "title": "Chinese",
                "description": "Asian inspired noodles",
                "created_at": "2024-06-01T09:17:57.661Z",
                "last_updated": "2024-06-01T09:17:57.661Z",
            }
        }
