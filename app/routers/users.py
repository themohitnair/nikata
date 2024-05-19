from fastapi import (
    APIRouter,
    status,
    HTTPException,
)
from pydantic import BaseModel
from typing import Literal, List

from bson import ObjectId
from pymongo import ReturnDocument

from app.database import db
from app.db_models import UserModel, PyObjectId

router = APIRouter()

@router.put(
    "/users/",
    tags=["users"],
    response_description="The added user",
    response_model=UserModel,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def add_user(new_user_payload: UserModel):
    new_user = await db.users.insert_one(
        new_user_payload.model_dump(by_alias=True, exclude={"id"})
    )
    created_user = await db.users.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user


class PatchPayload(BaseModel):
    id: PyObjectId
    operation: Literal["add", "remove"]
    field_name: str
    value: str | list[int] | list[str]


# TODO:
#  - Documentation for all endpoints (docstrings are enough coz fastapi gets them to the swagger ui as well).
#  - Code review with Mo.


@router.patch(
    "/users/",
    tags=["users"],
    response_description="The modified user",
    response_model=UserModel,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
)
async def update_user(update_payload: PatchPayload):
    user = await db.users.find_one({ "_id": ObjectId(update_payload.id) })
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if isinstance(update_payload.value, list)\
    and isinstance(update_payload.value[0], str):
        update_payload.value = [ObjectId(v) for v in update_payload.value]

    update_operations = {}
    if isinstance(update_payload.value, list):
        if update_payload.operation == "add":
            update_operations.update(
                {"$addToSet": { f"{update_payload.field_name}": { "$each": update_payload.value} } }
            )
        elif update_payload.operation == "remove":
            update_operations.update(
                {"$pullAll": { f"{update_payload.field_name}": update_payload.value} }
            )
    else:
        update_operations.update(
            {"$set": { f"{update_payload.field_name}": update_payload.value} }
        )

    updated_user = await db.users.find_one_and_update(
        { "_id": ObjectId(update_payload.id) },
        update_operations,
        return_document=ReturnDocument.AFTER
    )
    return updated_user


# shift to using ids?
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
