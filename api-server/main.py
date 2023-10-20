from typing import Annotated

from fastapi import Depends, FastAPI

# pylint: disable=import-error
from src.config.config import Settings
from src.controller.employee.endpoint import employee_router
from src.controller.enter_record.endpoint import enter_record_router
from src.controller.machine_record.endpoint import machine_record_router
from src.dependencies.settings import get_settings

app = FastAPI()
app.include_router(employee_router)
app.include_router(enter_record_router)
app.include_router(machine_record_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/envSettings")
def get_env_settings(settings: Annotated[Settings, Depends(get_settings)]):
    return {"db_host": settings.db_host, "db_port": settings.db_port}
