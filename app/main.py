from fastapi import FastAPI
from .routers import (
    users,
    geofences,
    chat_ids
)

app = FastAPI()

app.include_router(users.router)
app.include_router(geofences.router)
app.include_router(chat_ids.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Nikata Server!"}