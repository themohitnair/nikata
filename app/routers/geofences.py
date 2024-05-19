from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Response,
)
from pydantic import BaseModel
from bson import ObjectId

from app.db_models import (
    GeoFenceModel,
    GeoFenceCollection,
    PyObjectId,
)
from app.database import db, find_user

router = APIRouter()

@router.get(
    "/geofences/{user_name}",
    tags=["geofences"],
    response_description="Retrieved geofences",
    response_model=GeoFenceCollection,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
async def get_geofences(user_name: str):
    if (
        user := await find_user(user_name)
    ) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{user_name}' not found.")

    geofence_ids = list(map(ObjectId, user["geofence_ids"]))
    geofences_cursor = db.geofences.find(
        { "_id": { "$in": geofence_ids } }
    )
    geofences = [geofence async for geofence in geofences_cursor]
    if not geofences:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Geofences not found for user '{user_name}'.")

    return GeoFenceCollection(geofences=geofences)


@router.post(
    "/geofences/{user_name}",
    tags=["geofences"],
    response_description="The new geofence",
    response_model=GeoFenceModel,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED
)
async def add_geofence(user_name: str, geofence: GeoFenceModel, response: Response):
    if (await find_user(user_name)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{user_name}' not found.")

    new_geofence = await db.geofences.insert_one(
        geofence.model_dump(by_alias=True, exclude={"id"})
    )
    update_result = await db.users.update_one(
        { "name": user_name },
        { "$addToSet": { "geofence_ids": new_geofence.inserted_id } }
    )

    geofence.id = PyObjectId(new_geofence.inserted_id)
    return geofence


class DeleteRequestModel(BaseModel):
    geofence_id: PyObjectId
    user_id: PyObjectId


@router.delete(
    "/geofences/",
    tags=["geofences"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_geofence(delete_payload: DeleteRequestModel):
    if (
        await db.geofences.find_one_and_delete({ "_id": ObjectId(delete_payload.geofence_id)})
    ) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Geofence not found")

    await db.users.update_one(
        { "_id": ObjectId(delete_payload.user_id) },
        {
            "$pull": { "geofence_ids": ObjectId(delete_payload.geofence_id) }
        }
    )
