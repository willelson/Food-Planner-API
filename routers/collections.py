from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependecies.database import get_db
from dependecies.security import get_current_active_user
from models.collection_recipes import Collection as CollectionModel
from schemas.collection import Collection as CollectionSchema
from schemas.user import User as UserSchema

router = APIRouter(
    prefix="/collections",
    tags=["collections"],
)


@router.get("/", response_model=list[CollectionSchema])
async def read_user_collections(
    current_user: UserSchema = Depends(get_current_active_user),
):
    return current_user.collections


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection: CollectionSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):

    new_collection = CollectionModel(**collection.__dict__)
    new_collection.user_id = current_user.id

    db.add(new_collection)
    db.commit()
    db.refresh(new_collection)
    return collection


@router.get("/{collection_id}", response_model=CollectionSchema)
async def get_collection_by_id(
    collection_id: int,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    collection = (
        db.query(CollectionModel)
        .filter(
            CollectionModel.id == collection_id,
            CollectionModel.user_id == current_user.id,
        )
        .first()
    )

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )

    return collection
