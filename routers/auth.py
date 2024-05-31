from fastapi import APIRouter, Depends, HTTPException

from fastapi.security import OAuth2PasswordRequestForm

# from ..dependencies.security import get_token_header

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = "test-access-token"

    return {"access_token": access_token, "token_type": "bearer"}
