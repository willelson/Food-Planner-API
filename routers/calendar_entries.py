from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# from dependecies.collection_recipes import get_user_collection, get_user_recipe
from dependecies.database import get_db
from dependecies.security import get_current_active_user
from models.calendar_entry import CalendarEntry as CalendarEntryModel
from schemas.calendar_entry import CalendarEntry as CalendarEntrySchema
from schemas.calendar_entry import CalendarEntryCreate as CalendarEntryCreateSchema
from schemas.user import User as UserSchema

router = APIRouter(
    prefix="/calendar_entries",
    tags=["Calendar Entries"],
)


@router.get("/all", response_model=list[CalendarEntrySchema])
async def get_all_calendar_entries(db: Session = Depends(get_db)):
    calendar_entries = db.query(CalendarEntryModel).all()
    return calendar_entries


@router.get("/", response_model=list[CalendarEntrySchema])
async def read_user_calendar_entries(
    current_user: UserSchema = Depends(get_current_active_user),
):
    return current_user.calendar_entries


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_calendar_entry(
    calendar_entry: CalendarEntryCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    print("create calendar_entry")
    new_calendar_entry = CalendarEntryModel(**calendar_entry.__dict__)
    new_calendar_entry.user_id = current_user.id

    db.add(new_calendar_entry)
    db.commit()
    db.refresh(new_calendar_entry)
    return calendar_entry


@router.delete("/{calendar_entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_calendar_entry(
    calendar_entry_id: int,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    calendar_entry = (
        db.query(CalendarEntryModel)
        .filter(
            CalendarEntryModel.id == calendar_entry_id,
            CalendarEntryModel.user_id == current_user.id,
        )
        .first()
    )

    if not calendar_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Calendar entry not found"
        )

    db.delete(calendar_entry)
    db.commit()

    return {"message": "calendar entry successfully deleted"}


@router.get("/{calendar_id}", response_model=CalendarEntrySchema)
async def get_calendar_entry_by_id(
    calendar_id: int,
):
    return calendar_id
