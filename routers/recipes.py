from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.recipe import Recipe

router = APIRouter(prefix="/recipes", tags=["recipes"])


recipe1 = {
    "id": 9,
    "title": "Lasagne",
    "description": "A hearty Italian meal!",
    "source_url": "https://www.bbcgoodfood.com",
    "imageUrl": "https://www.example.com/test.png",
    "created_at": datetime.now(),
    "last_updated": datetime.now(),
    "collections": [],
}
recipe2 = {
    "id": 9,
    "title": "Curry",
    "description": "Rich and spicy!",
    "source_url": "https://www.bbcgoodfood.com",
    "imageUrl": "https://www.example.com/test.png",
    "created_at": datetime.now(),
    "last_updated": datetime.now(),
    "collections": [],
}

fake_recipes_db = {9: recipe1, 18: recipe2}


@router.get("/", response_model=list[Recipe])
async def read_user_recipes():
    return [recipe1, recipe2]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: Recipe):
    return recipe


@router.get("/{recipe}", response_model=Recipe)
async def get_recipe_by_id(recipe_id: int):
    recipe = fake_recipes_db.get(recipe_id)

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )

    return recipe
