from fastapi import FastAPI
from .routers import users, geofences

app = FastAPI()

app.include_router(users.router)
app.include_router(geofences.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Nikata Server!"}