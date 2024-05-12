from fastapi import (
    APIRouter,
    status,
    HTTPException,
)

from pydantic import BaseModel
from pymongo import ReturnDocument

from app.database import db
from app.db_models import UserModel
from app.database import find_user

router = APIRouter()

class ChatIDRequestModel(BaseModel):
    user_name: str
    chat_id: str


@router.put(
    "/chatid/",
    tags=["users"],
    response_description="Add a new telegram chat_id associated with an user.",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
)
async def add_chat_id(chatid_payload: ChatIDRequestModel):
    if (await find_user(chatid_payload.user_name)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{chatid_payload.user_name}' not found")

    updated_document = await db.users.find_one_and_update(
        { "name": chatid_payload.user_name},
        { "$addToSet": { "chat_ids": chatid_payload.chat_id}},
        return_document=ReturnDocument.AFTER
    )
    return updated_document

