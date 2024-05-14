from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator
)
from pydantic.functional_validators import BeforeValidator

from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    """
    Container for a single user record.
    """

    id: PyObjectId | None = Field(alias="_id", default=None)
    name: str
    email: EmailStr
    chat_ids: list[int]
    geofence_ids: list[PyObjectId]

class GeoJSONPoint(BaseModel):
    type: str = "Point"
    coordinates: tuple[float, float]

    @field_validator('coordinates')
    def validate_coordinates(cls, v):
        if not isinstance(v, tuple) or len(v) != 2:
            raise ValueError("Coordinates must be a tuple with two float values")
        longitude, latitude = v
        if not (-180 <= longitude <= 180) or not (-90 <= latitude <= 90):
            raise ValueError("Invalid coordinates: Longitude must be between -180 and 180, and latitude must be between -90 and 90 degrees")
        return v

class GeoFenceModel(BaseModel):
    """
    Container for a single geo fence record.
    """

    id: PyObjectId | None = Field(alias="_id", default=None)
    name: str
    coordinates: GeoJSONPoint
    radius: float

class GeoFenceCollection(BaseModel):
    """
    Container for a list of 'GeoFenceModel' instances.
    """

    geofences: list[GeoFenceModel]
