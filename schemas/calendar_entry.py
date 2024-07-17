from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .recipe import Recipe


class CalendarEntryBase(BaseModel):
    entry_date: datetime
    recipe_id: int


class CalendarEntryCreate(CalendarEntryBase):
    pass


class CalendarEntry(CalendarEntryBase):
    id: int
    user_id: int
    created_at: datetime
    recipe: Recipe

    class Config:
        from_attributes = True


class DateRange(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
