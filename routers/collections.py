from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy import asc
from sqlalchemy.orm import Session

from dependecies.collection_recipes import get_user_collection, get_user_recipe
from dependecies.database import get_db
from dependecies.security import get_current_active_user
from models.collection_recipes import Collection as CollectionModel
from models.collection_recipes import Recipe as RecipeModel
from models.collection_recipes import collection_recipes
from schemas.collection import Collection as CollectionSchema
from schemas.collection import CollectionCreate as CollectionCreateSchema
from schemas.collection import CollectionUpdate
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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CollectionSchema)
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
    return new_collection


@router.put(
    "/{collection_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=CollectionSchema,
)
async def update(
    collection: CollectionUpdate,
    current_collection: CollectionSchema = Depends(get_user_collection),
    db: Session = Depends(get_db),
):
    current_collection.title = collection.title
    db.commit()
    return current_collection


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


@router.post("/{collection_id}/recipes/{recipe_id}", response_model=CollectionSchema)
async def add_recipe_to_collection(
    recipe: RecipeModel = Depends(get_user_recipe),
    collection: CollectionModel = Depends(get_user_collection),
    db: Session = Depends(get_db),
):
    collection.recipes.append(recipe)

    if not collection.cover_image_url and recipe.image_url:
        collection.cover_image_url = recipe.image_url

    db.commit()

    return collection


@router.put("/{collection_id}/recipes")
async def add_collection_recipes(
    recipe_ids: Annotated[List[int], Body()],
    collection: CollectionModel = Depends(get_user_collection),
    db: Session = Depends(get_db),
):

    for recipe_id in recipe_ids:
        # Check collection does not already have this recipe
        collection_recipe = (
            db.query(collection_recipes)
            .filter(
                collection_recipes.c.recipe_id == recipe_id,
                collection_recipes.c.collection_id == collection.id,
            )
            .first()
        )

        if collection_recipe:
            continue

        recipe = db.query(RecipeModel).get(recipe_id)

        if not collection.cover_image_url:
            collection.cover_image_url = recipe.image_url

        collection.recipes.append(recipe)

    db.commit()


def get_new_collection_cover(
    db: Session, collection_id: int, current_first_recipe_id: int
):
    """
    Get the image of the first recipe in the collection to use as the collection cover image
    current_first_recipe_id is being removed from the collection so we exclude it from the query
    """

    first_collection_recipe = (
        db.query(collection_recipes)
        .filter(
            collection_recipes.c.collection_id == collection_id,
            collection_recipes.c.recipe_id != current_first_recipe_id,
        )
        .order_by(asc("created_at"))
        .first()
    )

    if not first_collection_recipe:
        return None

    first_recipe = db.query(RecipeModel).get(first_collection_recipe.recipe_id)
    return first_recipe.image_url


@router.delete(
    "/{collection_id}/recipes/{recipe_id}", status_code=status.HTTP_202_ACCEPTED
)
async def delete_recipe_from_collection(
    recipe: RecipeModel = Depends(get_user_recipe),
    collection: CollectionModel = Depends(get_user_collection),
    db: Session = Depends(get_db),
):
    collection.recipes.remove(recipe)

    if collection.cover_image_url == recipe.image_url:
        # Update collection cover image url
        collection.cover_image_url = get_new_collection_cover(
            db, collection.id, recipe.id
        )

    db.commit()


@router.delete("/{collection_id}/recipes")
async def delete_collection_recipes(
    recipe_ids: Annotated[List[int], Body()],
    collection: CollectionModel = Depends(get_user_collection),
    db: Session = Depends(get_db),
):

    for recipe_id in recipe_ids:
        recipe = db.query(RecipeModel).get(recipe_id)
        collection.recipes.remove(recipe)

        if collection.cover_image_url == recipe.image_url:
            # Update collection cover image url
            collection.cover_image_url = get_new_collection_cover(
                db, collection.id, recipe.id
            )

    db.commit()
