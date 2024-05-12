from fastapi import (
    APIRouter,
    status,
    HTTPException,
)

from app.database import db
from app.db_models import UserModel

router = APIRouter()

@router.post(
    "/users/",
    tags=["users"],
    response_description="Add a new user.",
    response_model=UserModel,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def add_user(user_deets: UserModel):
    new_user = await db.users.insert_one(
        user_deets.model_dump(by_alias=True, exclude={"id"})
    )
    created_user = await db.users.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user


@router.delete(
    "/users/{user_name}",
    tags=["users"],
    response_description="Delete a student.",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(user_name: str):
    delete_result = await db.users.delete_one(
        {"name": user_name}
    )
    if delete_result.deleted_count != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{user_name}' not found")
