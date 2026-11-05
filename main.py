from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sqlalchemy_file.storage import StorageManager

from libcloud.storage.drivers.local import LocalStorageDriver

from routers.users import router as users_router

from db.database import create_db, engine

from admin.admin_config import admin_setup


import uvicorn
import os


app = FastAPI()

app.mount("/static", 
          StaticFiles(directory="static"), 
          name="static")

app.include_router(users_router)


os.makedirs("./files", 0o777, exist_ok=True)
container = LocalStorageDriver("./files").get_container("sight_picture")
StorageManager.add_storage("default", container)


admin_setup(app, engine)


if __name__ == "__main__":
    create_db()
    uvicorn.run("main:app", 
                port=5000, 
                log_level="info")