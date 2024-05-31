from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

# from ..models.collection import Collection

router = APIRouter(prefix="/collections", tags=["collections"])


collection1 = {
    "id": 12,
    "title": "Summer",
    "description": "Light and easy meals",
    "created_at": datetime.now(),
    "last_updated": datetime.now(),
    "recipes": [],
}
collection2 = {
    "id": 33,
    "title": "Chineese",
    "description": "Asian inspired noodles",
    "created_at": datetime.now(),
    "last_updated": datetime.now(),
    "recipes": [],
}


@router.get("/")
async def read_user_collections():
    return {"collections": [collection1, collection2]}


@router.post("/")
async def create_collection():
    return {"collections": ["collection 1", "collection 2"]}


@router.get("/{collection_id}")
async def get_collection_by_id(collection_id: int):
    return {"collection": collection1, "collection_id": collection_id}
