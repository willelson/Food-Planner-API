from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependecies.collection_recipes import get_user_collection, get_user_recipe
from dependecies.database import get_db
from dependecies.security import get_current_active_user
from models.collection_recipes import Collection as CollectionModel
from models.collection_recipes import Recipe as RecipeModel
from models.collection_recipes import collection_recipes
from schemas.collection import Collection as CollectionSchema
from schemas.collection import CollectionCreate as CollectionCreateSchema
from schemas.recipe import Recipe as RecipeSchema
from schemas.user import User as UserSchema

router = APIRouter(
    prefix="/collections",
    tags=["Collections"],
)


@router.get("/", response_model=list[CollectionSchema])
async def read_user_collections(
    query: str = "",
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    collections = (
        db.query(CollectionModel)
        .filter(
            CollectionModel.user_id == current_user.id,
            CollectionModel.title.ilike(f"%{query}%"),
        )
        .all()
    )

    return collections


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection: CollectionCreateSchema,
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
    collection: CollectionModel = Depends(get_user_collection),
):
    return collection


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    collection: CollectionModel = Depends(get_user_collection),
    db: Session = Depends(get_db),
):
    db.delete(collection)
    db.commit()

    return {"message": "collection successfully deleted"}


@router.get("/{collection_id}/recipes", response_model=list[RecipeSchema])
async def read_collection_recipes(
    query: str = "",
    collection: CollectionModel = Depends(get_user_collection),
    db: Session = Depends(get_db),
):
    recipes_query = (
        db.query(RecipeModel)
        .join(collection_recipes)
        .filter(collection_recipes.c.collection_id == collection.id)
    )

    if query:
        recipes_query = recipes_query.filter(RecipeModel.title.ilike(f"%{query}%"))

    recipes = recipes_query.all()
    return recipes


@router.post(
    "/{collection_id}/recipes/{recipe_id}",
)
async def add_recipe_to_collection(
    recipe: RecipeModel = Depends(get_user_recipe),
    collection: CollectionModel = Depends(get_user_collection),
    db: Session = Depends(get_db),
):
    collection.recipes.append(recipe)
    db.commit()


@router.delete(
    "/{collection_id}/recipes/{recipe_id}", status_code=status.HTTP_202_ACCEPTED
)
async def delete_recipe_from_collection(
    recipe: RecipeModel = Depends(get_user_recipe),
    collection: CollectionModel = Depends(get_user_collection),
    db: Session = Depends(get_db),
):
    collection.recipes.remove(recipe)
    db.commit()
