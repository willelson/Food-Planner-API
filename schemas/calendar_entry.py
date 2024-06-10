from datetime import datetime

from pydantic import BaseModel

from .recipe import Recipe


class CalendarEntryBase(BaseModel):
    entry_date: datetime
    created_at: datetime
    recipe_id: int


class CalendarEntryCreate(CalendarEntryBase):
    pass


class CalendarEntry(CalendarEntryBase):
    id: int
    user_id: int
    recipe: Recipe

    class Config:
        from_attributes = True
