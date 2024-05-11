from fastapi import (
    APIRouter,
    status,
    HTTPException,
)
from pydantic import BaseModel
from bson import ObjectId

from app.db_models import (
    GeoFenceModel,
    GeoFenceCollection,
    PyObjectId
)
from app.database import db, find_user

router = APIRouter()

@router.get(
    "/geofences/{user_name}",
    tags=["geofences"],
    response_description="Retrieve a user's geofences.",
    response_model=GeoFenceCollection,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
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
    if geofences:
        return GeoFenceCollection(geofences=geofences)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Geofences not found for user '{user_name}'.")


# @router.put(
#     "/geofences/{geofence_name}",
#     tags=["geofences"],
#     response_description="Update a geofence by name.",
#     response_model=GeoFenceModel,
# )
# async def update_geofence()


@router.post(
    "/geofences/{user_name}",
    tags=["geofences"],
    response_description="Add a new geofence.",
    response_model=GeoFenceModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def add_geofence(user_name: str, geofence: GeoFenceModel):
    if (await find_user(user_name)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{user_name}' not found.")

    new_geofence = await db.geofences.insert_one(
        geofence.model_dump(by_alias=True, exclude={"id"})
    )
    await db.users.update_one(
        { "name": user_name },
        { "$addToSet": { "geofence_ids": new_geofence.inserted_id } }
    )
    geofence.id = PyObjectId(new_geofence.inserted_id)
    return geofence


class DeleteRequestModel(BaseModel):
    geofence_id: PyObjectId
    user_name: str


@router.delete(
    "/geofences/",
    tags=["geofences"],
    response_description="Delete a geofence.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_geofence(delete_deets: DeleteRequestModel):
    if (
        geofence := await db.geofences.find_one_and_delete({ "_id": ObjectId(delete_deets.geofence_id) })
    ) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Geofence not found")

    await db.users.update_one(
        { "name": delete_deets.user_name },
        {
            "$pull": { "geofence_ids": ObjectId(delete_deets.geofence_id) }
        }
    )
