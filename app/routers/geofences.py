from fastapi import APIRouter, status, HTTPException, Response
from app.db_models import GeoFenceModel, GeoFenceCollection
from app.database import db

from bson import ObjectId

router = APIRouter()

@router.get(
    "/geofences/{user_name}",
    tags=["geofences"],
    response_description="Retrieve a user's geofences.",
    response_model=GeoFenceCollection,
    response_model_by_alias=False,
)
async def get_geofences(user_name: str):
    if (
        user := await db.users.find_one({"name": user_name})
    ) is None:
        raise HTTPException(status_code=404, detail=f"User '{user_name}' not found.")

    geofence_ids = list(map(ObjectId, user["geofence_ids"]))
    geofences_cursor = db.geofences.find(
        {"_id": {"$in": geofence_ids}}
    )
    geofences = [geofence async for geofence in geofences_cursor]
    if geofences:
        return GeoFenceCollection(geofences=geofences)

    raise HTTPException(status_code=404, detail=f"Geofences not found for user '{user_name}'.")


# @router.put(
#     "/geofences/{geofence_name}",
#     tags=["geofences"],
#     response_description="Update a geofence by name.",
#     response_model=GeoFenceModel,
# )
# async


@router.post(
    "/geofences/{user_name}",
    tags=["geofences"],
    response_description="Add a new geofence.",
    response_model=GeoFenceModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def add_geofence(user_name: str, geofence: GeoFenceModel):
    new_geofence = await db.geofences.insert_one(
        geofence.model_dump(by_alias=True, exclude={"id"})
    )
    # TODO: Update the 'user_name' user's 'geofence_ids' field to include the created geofence's id
    created_geofence = await db.geofences.find_one(
        {"_id": new_geofence.inserted_id}
    )
    return created_geofence


@router.delete(
    "/geofences/{geofence_name}",
    tags=["geofences"],
    response_description="Delete a geofence.",
)
async def delete_geofences(geofence_name: str):
    delete_result = await db.geofences.delete_one(
        {"name": geofence_name}
    )
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Geofence {geofence_name} not found")
