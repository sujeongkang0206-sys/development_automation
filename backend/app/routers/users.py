import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status

from app import crud, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.UserResponse])
async def read_users(offset: int = 0, limit: int = 20):
    return await crud.get_users(skip=offset, limit=limit)


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: str):
    user = await crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: schemas.UserCreate):
    existing = await crud.get_user_by_email(user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = await crud.create_user(user_in=user_in, user_id=str(uuid.uuid4()))
    return user


@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: str, user_update: schemas.UserUpdate):
    user = await crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await crud.update_user(user, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    user = await crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await crud.delete_user(user_id)
