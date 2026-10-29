from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sqlalchemy_file.storage import StorageManager

from libcloud.storage.drivers.local import LocalStorageDriver

from routers.users import router as users_router


import uvicorn
import os


app = FastAPI()

app.mount("/static", 
          StaticFiles(directory="static"), 
          name="static")

app.include_router(users_router)


os.makedirs("./files", 0o777, exist_ok=True)
container = LocalStorageDriver("./files").get_container("images")
StorageManager.add_storage("default", container)


if __name__ == "__main__":
    uvicorn.run("main:app", 
                port=5000, 
                log_level="info")