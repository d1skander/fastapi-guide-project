from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sqlalchemy_file.storage import StorageManager

from libcloud.storage.drivers.local import LocalStorageDriver

from routers.users import router as users_router
from routers.main import router as main_router

from db.database import create_db, engine

from admin.admin_config import admin_setup


import uvicorn
import os


app = FastAPI()

app.mount("/files/info_picture", StaticFiles(directory="./files/info_picture"), name="info_picture_files")

app.mount("/static", 
          StaticFiles(directory="static"), 
          name="static")
app.mount("/files",
          StaticFiles(directory="files"),
          name="files")

app.include_router(users_router)
app.include_router(main_router)


os.makedirs("./files", 0o777, exist_ok=True)
container_sight = LocalStorageDriver("./files").get_container("sight_picture")
container_info = LocalStorageDriver("./files").get_container("info_picture")
StorageManager.add_storage("storage_sight", container_sight)
StorageManager.add_storage("storage_info", container_info)


admin_setup(app, engine)


if __name__ == "__main__":
    create_db()
    uvicorn.run("main:app", 
                port=5000, 
                log_level="info")