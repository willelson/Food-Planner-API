from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependecies.database import get_db
from dependecies.security import get_current_active_user
from models.collection_recipes import Collection as CollectionModel
from models.collection_recipes import Recipe as RecipeModel
from schemas.user import User as UserSchema


async def get_user_recipe(
    recipe_id: int,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    recipe = (
        db.query(RecipeModel)
        .filter(
            RecipeModel.id == recipe_id,
            RecipeModel.user_id == current_user.id,
        )
        .first()
    )

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )

    return recipe


async def get_user_collection(
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
