from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/")
async def read_user_recipes():
    return {"recipes": ["recipe 1", "recipe 2"]}


@router.post("/")
async def create_recipe():
    return {"recipes": ["recipe 1", "recipe 2"]}


@router.get("/{recipe_id}")
async def get_recipe_by_id():
    return {"recipe": "recipe 1"}
