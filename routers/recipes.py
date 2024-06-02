from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependecies.collection_recipes import get_user_recipe
from dependecies.database import get_db
from dependecies.security import get_current_active_user
from models.collection_recipes import Recipe as RecipeModel
from schemas.recipe import Recipe as RecipeSchema
from schemas.recipe import RecipeCreate as RecipeCreateSchema
from schemas.user import User as UserSchema

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/", response_model=list[RecipeSchema])
async def read_user_recipes(
    current_user: UserSchema = Depends(get_current_active_user),
):
    return current_user.recipes


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe: RecipeCreateSchema,
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
    recipe: RecipeModel = Depends(get_user_recipe),
):
    return recipe
