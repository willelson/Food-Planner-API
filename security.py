from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from schemas.user import UserInDB

SECRET_KEY = "move-this-to-an-environemnt-variable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    print(f"get_user - username = {username}")
    if username in db:
        user_dict = db[username]
        print(user_dict)
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):

    user = get_user(fake_users_db, username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        print("verify password return false")
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
