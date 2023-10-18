from typing import Annotated

from fastapi import Depends, FastAPI

# pylint: disable=import-error
from src.config.config import Settings
from src.controller.user.endpoint import user_router
from src.dependencies.settings import get_settings

app = FastAPI()
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/envSettings")
def get_env_settings(settings: Annotated[Settings, Depends(get_settings)]):
    return {"db_host": settings.db_host, "db_port": settings.db_port}
