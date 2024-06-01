from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependecies.database import get_db
from dependecies.security import get_current_active_user
from models.collection_recipes import Recipe as RecipeModel
from schemas.recipe import Recipe as RecipeSchema
from schemas.user import User as UserSchema

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=list[RecipeSchema])
async def read_user_recipes(
    current_user: UserSchema = Depends(get_current_active_user),
):
    return current_user.recipes


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe: RecipeSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):

    new_recipe = RecipeModel(**recipe.__dict__)
    new_recipe.user_id = current_user.id

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return recipe


@router.get("/{recipe_id}", response_model=RecipeSchema)
async def get_recipe_by_id(
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
