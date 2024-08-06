from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from PIL import Image
from sqlalchemy.orm import Session

from dependecies.collection_recipes import get_user_recipe
from dependecies.database import get_db
from dependecies.security import get_current_active_user
from models.collection_recipes import Recipe as RecipeModel
from models.collection_recipes import collection_recipes
from schemas.recipe import Recipe as RecipeSchema
from schemas.recipe import RecipeCreate as RecipeCreateSchema
from schemas.recipe import RecipeUpdate as RecipeUpdateSchema
from schemas.user import User as UserSchema

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/", response_model=list[RecipeSchema])
async def read_user_recipes(
    query: str = "",
    collection_id: int | None = None,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    query = db.query(RecipeModel).filter(
        RecipeModel.user_id == current_user.id, RecipeModel.title.like(f"%{query}%")
    )

    if collection_id:
        print(f"collection_id = {collection_id}")
        query = query.join(collection_recipes).filter(
            collection_recipes.c.collection_id == collection_id
        )

    return query.all()


@router.get(
    "/image/{image_path}",
    response_class=FileResponse,
)
async def get_recipe_image(image_path: str):
    file_location = f"user_images/{image_path}"
    return FileResponse(file_location)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_recipe(
    title: str = Form(),
    image: UploadFile = File(None),
    description: str = Form(None),
    source_url: str = Form(None),
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    recipeData = {
        "title": title,
        "description": description or "",
        "source_url": source_url or "",
    }

    if description:
        recipeData["description"] = description

    if source_url:
        recipeData["source_url"] = source_url

    new_recipe = RecipeModel(**recipeData)
    new_recipe.user_id = current_user.id

    if image:
        file_location = f"user_images/{image.filename}"

        try:
            im = Image.open(image.file)
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB")
            im.save(file_location, "JPEG", quality=50)
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
        finally:
            image.file.close()
            im.close()

        new_recipe.image_url = f"recipes/image/{image.filename}"

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


@router.put(
    "/{recipe_id}", status_code=status.HTTP_202_ACCEPTED, response_model=RecipeSchema
)
async def update_recipe(
    updated_recipe: RecipeUpdateSchema,
    current_recipe: RecipeModel = Depends(get_user_recipe),
    db: Session = Depends(get_db),
):
    for [column, value] in updated_recipe.__dict__.items():
        setattr(current_recipe, column, value)

    db.commit()

    return current_recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe: RecipeModel = Depends(get_user_recipe),
    db: Session = Depends(get_db),
):
    db.delete(recipe)
    db.commit()

    return {"message": "recipe successfully deleted"}


@router.get("/{recipe_id}", response_model=RecipeSchema)
async def get_recipe_by_id(
    recipe: RecipeModel = Depends(get_user_recipe),
):
    return recipe
