from pydantic import BaseModel


class CalendarEntryBase(BaseModel):
    entry_date: str
    created_at: str | None = None
    recipe: int


class CalendarEntryCreate(CalendarEntryBase):
    pass


class CalendarEntry(CalendarEntryBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
