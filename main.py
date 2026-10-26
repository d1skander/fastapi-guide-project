from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers.users import router as users_router


import uvicorn


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")