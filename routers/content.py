from fastapi import APIRouter, Depends

from data_processors.factory import data_processor
from dependecies.security import get_current_active_user
from schemas.content import Content as ContentSchema
from schemas.user import User as UserSchema

router = APIRouter(prefix="/content", tags=["Content"])


@router.get("/", response_model=ContentSchema)
async def get_content_preview(
    url: str = "",
    current_user: UserSchema = Depends(get_current_active_user),
):
    return data_processor(url)
