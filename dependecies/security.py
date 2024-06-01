import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from dependecies.database import get_db
from schemas.token import TokenData
from schemas.user import User
from security import ALGORITHM, SECRET_KEY, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # Define exception to return for invalid credenetials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode token to read username - raise exception if no username provided
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    # Find user in fake users db - this will be replaced by a database look up...
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Takes current user and checks if the account is marked as disabled"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
