from fastapi import FastAPI
from pydantic import BaseModel
from locationpoll import Client

app = FastAPI()

clients: dict[str, Client] = {}

class CoordinatesInput(BaseModel):
    name: str
    center_coordinates: tuple[float, float]
    curr_coordinates: tuple[float, float]
    radius: int
    chat_ids: list[str]
    geoname: str


@app.post("/adopt-info/")
async def process_coordinates(user_info: CoordinatesInput):
    request_body = user_info.dict()
    name = request_body.pop('name')

    if name in clients:
        client = clients[name]
    else:
        client = Client(request_body)
        clients[name] = client

    client.change_state()
    client.trigger()

    # more to be done here
    # tbd later
    return {"message": "success yay"} #tbd if success message is even required; depends on client-side verification of telegram chatIDs
