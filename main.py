from fastapi import FastAPI, Depends

from routers.recipes import router as recipes_router
from routers.collections import router as collections_router
from routers.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(recipes_router)
app.include_router(collections_router)


@app.get("/")
async def root():
    return {"message": "Hello bigger applications"}
