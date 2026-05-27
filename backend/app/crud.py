import hashlib
from datetime import datetime
from typing import Dict, List, Optional

from app import schemas

_store: Dict[str, Dict] = {}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


async def get_user(user_id: str) -> Optional[Dict]:
    return _store.get(user_id)


async def get_user_by_email(email: str) -> Optional[Dict]:
    return next((user for user in _store.values() if user["email"] == email), None)


async def get_users(skip: int = 0, limit: int = 100) -> List[Dict]:
    users = list(_store.values())
    return users[skip : skip + limit]


async def create_user(user_in: schemas.UserCreate, user_id: str) -> Dict:
    user = {
        "id": user_id,
        "email": user_in.email,
        "full_name": user_in.full_name,
        "is_active": user_in.is_active,
        "created_at": datetime.utcnow(),
        "hashed_password": hash_password(user_in.password),
    }
    _store[user_id] = user
    return user


async def update_user(user: Dict, updates: schemas.UserUpdate) -> Dict:
    if updates.email is not None:
        user["email"] = updates.email
    if updates.full_name is not None:
        user["full_name"] = updates.full_name
    if updates.is_active is not None:
        user["is_active"] = updates.is_active
    return user


async def delete_user(user_id: str) -> None:
    _store.pop(user_id, None)
