from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.collection import Collection

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

fake_collections_db = {12: collection1, 33: collection2}


@router.get("/", response_model=list[Collection])
async def read_user_collections():
    return [collection1, collection2]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_collection(collection: Collection):
    return collection


@router.get("/{collection_id}", response_model=Collection)
async def get_collection_by_id(collection_id: int):
    collection = fake_collections_db.get(collection_id)

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )

    return collection
