from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore

from a2wsgi import WSGIMiddleware

from routers.users import router as users_router


import uvicorn


fs_store = HttpExposedFileSystemStore(path="images", 
                                      prefix="picture/")

fs_store_wsgi = fs_store.wsgi_middleware(lambda environ, start_response: start_response('404 Not Found', []) or [])# ИИ помог, не мог разобраться, как обернуть wsgi в asgi(((


app = FastAPI()

app.mount("/static", 
          StaticFiles(directory="static"), 
          name="static")

app.mount("/images", WSGIMiddleware(fs_store_wsgi))# ИИ помог, не мог разобраться, как обернуть wsgi в asgi(((

app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", 
                port=5000, 
                log_level="info")