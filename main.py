from dotenv import load_dotenv
from fastapi import FastAPI

from database import Base, engine
from routers.auth import router as auth_router
from routers.calendar_entries import router as calendar_entries_router
from routers.collections import router as collections_router
from routers.recipes import router as recipes_router

load_dotenv()

# Using declarative base - this updates tables to reflect our models
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(recipes_router)
app.include_router(collections_router)
app.include_router(calendar_entries_router)
