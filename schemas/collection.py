from datetime import datetime

from pydantic import BaseModel


class CollectionBase(BaseModel):
    title: str
    description: str | None = None


class CollectionCreate(CollectionBase):
    pass


class Collection(CollectionBase):
    id: int
    created_at: datetime
    last_updated: datetime
    cover_image_url: str | None = None

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "id": 33,
                "title": "Chinese",
                "description": "Asian inspired noodles",
                "created_at": "2024-06-01T09:17:57.661Z",
                "last_updated": "2024-06-01T09:17:57.661Z",
                "cover_image_url": "http://localhost:8080/collections/cover_image",
            }
        }
